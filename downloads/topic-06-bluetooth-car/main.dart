import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'package:google_fonts/google_fonts.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Pico Car Controller',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blueAccent),
        useMaterial3: true,
        textTheme: GoogleFonts.robotoTextTheme(),
      ),
      home: const BluetoothScanScreen(),
    );
  }
}

class BluetoothScanScreen extends StatefulWidget {
  const BluetoothScanScreen({super.key});

  @override
  State<BluetoothScanScreen> createState() => _BluetoothScanScreenState();
}

class _BluetoothScanScreenState extends State<BluetoothScanScreen> {
  // 掃描結果列表
  List<ScanResult> scanResults = [];
  bool isScanning = false;

  @override
  void initState() {
    super.initState();
    // 監聽掃描狀態
    FlutterBluePlus.isScanning.listen((state) {
      if (mounted) {
        setState(() {
          isScanning = state;
        });
      }
    });
    
    // 監聽掃描結果
// 監聽掃描結果
    FlutterBluePlus.scanResults.listen((results) {
      if (mounted) {
        setState(() {
          // 修改處：使用 where 過濾，只保留 platformName 不為空的裝置
          scanResults = results
              .where((r) => r.device.platformName.isNotEmpty)
              .toList();
        });
      }
    });
  }

Future<void> startScan() async {
    try {
      await FlutterBluePlus.stopScan();
      debugPrint("開始搜尋 PicoCar...");

      await FlutterBluePlus.startScan(
        // 1. 只搜尋新名字
        withNames: ["PicoCar"], 
        
        // 2. 搜尋新設定的 UUID (FFA0)
        // 雖然晶片改了，但建議還是保留 FFE0 以防改寫失敗時還能連上
        withServices: [
          Guid("FFA0"), // 這是您剛剛寫入的新設定
          Guid("FFE0")  // 備用 (原廠預設)
        ],
        
        timeout: const Duration(seconds: 15),
      );
    } catch (e) {
      debugPrint("搜尋錯誤: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("搜尋 Pico 小車")),
      body: Column(
        children: [
          if (scanResults.isEmpty && !isScanning)
            const Expanded(child: Center(child: Text("點擊按鈕開始搜尋藍牙裝置"))),
          Expanded(
            child: ListView.builder(
              itemCount: scanResults.length,
              itemBuilder: (context, index) {
                final device = scanResults[index].device;
                final name = device.platformName.isNotEmpty ? device.platformName : "Unknown Device";
                return Card(
                  margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  child: ListTile(
                    title: Text(name, style: const TextStyle(fontWeight: FontWeight.bold)),
                    subtitle: Text(device.remoteId.toString()),
                    trailing: const Icon(Icons.bluetooth),
                    onTap: () {
                      // 停止掃描並跳轉到控制頁面
                      FlutterBluePlus.stopScan();
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (context) => ControllerScreen(device: device)),
                      );
                    },
                  ),
                );
              },
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: isScanning ? FlutterBluePlus.stopScan : startScan,
        label: Text(isScanning ? "停止搜尋" : "搜尋裝置"),
        icon: Icon(isScanning ? Icons.stop : Icons.search),
      ),
    );
  }
}

class ControllerScreen extends StatefulWidget {
  final BluetoothDevice device;
  const ControllerScreen({super.key, required this.device});

  @override
  State<ControllerScreen> createState() => _ControllerScreenState();
}

class _ControllerScreenState extends State<ControllerScreen> {
  BluetoothCharacteristic? writeCharacteristic;
  String connectionStatus = "Connecting...";
  bool isReady = false;

  @override
  void initState() {
    super.initState();
    connectToDevice();
  }

  Future<void> connectToDevice() async {
    try {
      await widget.device.connect();
      setState(() => connectionStatus = "Discovering Services...");

      List<BluetoothService> services = await widget.device.discoverServices();
      
      // --- 修改重點 1: 精準尋找正確的特徵值 ---
      BluetoothCharacteristic? targetChar;

      for (var service in services) {
        for (var characteristic in service.characteristics) {
          String uuid = characteristic.uuid.toString().toLowerCase();
          
          // 優先尋找標準的 UART 通道 (FFE1 或 FFA1)
          if (uuid.contains("ffe1") || uuid.contains("ffa1")) {
             targetChar = characteristic;
             break;
          }
          
          // 如果還沒找到，先暫存任何可以寫入的通道當備案
          if (characteristic.properties.write || characteristic.properties.writeWithoutResponse) {
            if (targetChar == null) {
              targetChar = characteristic;
            }
          }
        }
        if (targetChar != null && (targetChar.uuid.toString().contains("ffe1") || targetChar.uuid.toString().contains("ffa1"))) {
          break; // 找到最佳解，跳出迴圈
        }
      }
      
      if (targetChar != null) {
        writeCharacteristic = targetChar;
        setState(() {
          connectionStatus = "Connected to ${widget.device.platformName}\nTarget: ${targetChar!.uuid}";
          isReady = true;
        });
      } else {
        setState(() => connectionStatus = "Error: No writable characteristic found");
      }

    } catch (e) {
      setState(() => connectionStatus = "Connection Failed: $e");
    }
  }

  Future<void> sendCommand(String cmd) async {
    if (writeCharacteristic == null) return;
    try {
      // --- 修改重點 2: 解決 GATT operation not permitted ---
      // 判斷是否支援 "writeWithoutResponse" (快速模式)
      // 很多便宜的藍牙模組只支援這個，如果用錯模式就會報錯！
      bool useWithoutResponse = writeCharacteristic!.properties.writeWithoutResponse;
      
      await writeCharacteristic!.write(
        utf8.encode(cmd), 
        withoutResponse: useWithoutResponse // 自動切換模式
      );
      
      debugPrint("Sent: $cmd (Mode: ${useWithoutResponse ? 'NoResp' : 'Resp'})");
      
    } catch (e) {
      debugPrint("Send Error: $e");
      // 如果發生錯誤，更新狀態讓使用者知道
      setState(() => connectionStatus = "Send Error: $e");
    }
  }

  @override
  void dispose() {
    widget.device.disconnect();
    super.dispose();
  }

  Widget buildControlBtn(String label, IconData icon, String cmdColor, String command) {
    return GestureDetector(
      onTapDown: (_) => sendCommand(command),
      onTapUp: (_) => sendCommand("0"),
      onTapCancel: () => sendCommand("0"),
      child: Container(
        width: 80,
        height: 80,
        decoration: BoxDecoration(
          color: Colors.blue.shade100,
          shape: BoxShape.circle,
          border: Border.all(color: Colors.blue, width: 2),
        ),
        child: Icon(icon, size: 40, color: Colors.blue.shade900),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("控制器")),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(connectionStatus, 
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 14, color: Colors.grey)),
            ),
            const SizedBox(height: 20),
            if (isReady) ...[
              buildControlBtn("Forward", Icons.arrow_upward, "blue", "1"),
              const SizedBox(height: 20),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  buildControlBtn("Left", Icons.arrow_back, "blue", "3"),
                  const SizedBox(width: 20),
                  FloatingActionButton(
                    backgroundColor: Colors.red,
                    onPressed: () => sendCommand("0"),
                    child: const Icon(Icons.stop, color: Colors.white),
                  ),
                  const SizedBox(width: 20),
                  buildControlBtn("Right", Icons.arrow_forward, "blue", "4"),
                ],
              ),
              const SizedBox(height: 20),
              buildControlBtn("Backward", Icons.arrow_downward, "blue", "2"),
            ]
          ],
        ),
      ),
    );
  }
}