//import 'dart:ffi';

import 'package:flutter/material.dart';
import 'package:stenoid_stt/shortcut.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Stenoid',
      theme: ThemeData(
        // This is the theme of your application.
        //
        // TRY THIS: Try running your application with "flutter run". You'll see
        // the application has a purple toolbar. Then, without quitting the app,
        // try changing the seedColor in the colorScheme below to Colors.green
        // and then invoke "hot reload" (save your changes or press the "hot
        // reload" button in a Flutter-supported IDE, or press "r" if you used
        // the command line to start the app).
        //
        // Notice that the counter didn't reset back to zero; the application
        // state is not lost during the reload. To reset the state, use hot
        // restart instead.
        //
        // This works for code too, not just values: Most code changes can be
        // tested with just a hot reload.
        colorScheme: ColorScheme.fromSeed(seedColor: Color.fromARGB(255, 170, 72, 72)),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Stenoid STT'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  double pdBtn = 10;
  double pdColumn = 8;
  double pdWinBorder = 20;
  double iconSize = 24;
  double iconSizeLarge = 40;

  String text_ex = printMessage("Example of Message");

  Size btnDefault = const Size(150, 50);

  void _doRecord() {
    setState(() {
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text(
              'You can edit the result after voice input has done.',
              style: TextStyle(
                fontSize: 10,
              ),
            ),
            Padding(
              padding: EdgeInsets.all(pdWinBorder), // 원하는 패딩 값으로 조절 가능
              child: const TextField(
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: 'Input',
                ),
              ),
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center, // 가로 축에서의 정렬 방식
              children: <Widget>[
                SizedBox(width: pdWinBorder),
                Column( //record, pause, and stop
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: <Widget>[
                    ElevatedButton(
                      onPressed: () {
                        final snackBar = SnackBar(
                          content: Text(text_ex),
                        );
                        
                        // ScaffoldMessenger를 사용하여 SnackBar를 현재 context에 표시
                        ScaffoldMessenger.of(context).showSnackBar(snackBar);
                      },
                      style: ElevatedButton.styleFrom(
                        minimumSize: btnDefault, // 버튼의 최소 크기를 200x50으로 설정
                      ),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.start,
                        children: <Widget>[
                          Icon(
                            Icons.radio_button_checked,
                            color: Color.fromARGB(255, 233, 30, 30),
                            size: iconSize,
                            fill: 1,
                          ),
                          SizedBox(width: pdBtn, height: pdBtn), // 버튼 사이의 간격
                          const Text('Record'),
                        ]
                      )
                    ),
                    SizedBox(width: pdBtn, height: pdBtn), // 버튼 사이의 간격
                    ElevatedButton(
                      onPressed: () {
                      },
                      style: ElevatedButton.styleFrom(
                        minimumSize: btnDefault, // 버튼의 최소 크기를 200x50으로 설정
                      ),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.start,
                        children: <Widget>[
                          Icon(
                            Icons.pause,
                            size: iconSize,
                            fill: 1,
                          ),
                          SizedBox(width: pdBtn, height: pdBtn), // 버튼 사이의 간격
                          const Text('Pause'),
                        ]
                      )
                    ),
                    SizedBox(width: pdBtn, height: pdBtn), // 버튼 사이의 간격
                    ElevatedButton(
                      onPressed: () {
                      },
                      style: ElevatedButton.styleFrom(
                        minimumSize: btnDefault, // 버튼의 최소 크기를 200x50으로 설정
                      ),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.start,
                        children: <Widget>[
                          Icon(
                            Icons.stop,
                            size: iconSize,
                            fill: 1,
                          ),
                          SizedBox(width: pdBtn, height: pdBtn), // 버튼 사이의 간격
                          const Text('Stop'),
                        ]
                      )
                    ),
                    SizedBox(width: pdBtn, height: pdBtn), // 버튼 사이의 간격
                    ElevatedButton(
                      onPressed: () {
                      },
                      style: ElevatedButton.styleFrom(
                        minimumSize: btnDefault, // 버튼의 최소 크기를 200x50으로 설정
                      ),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.start,
                        children: <Widget>[
                          Icon(
                            Icons.translate,
                            size: iconSize,
                            fill: 1,
                          ),
                          SizedBox(width: pdBtn, height: pdBtn), // 버튼 사이의 간격
                          const Text('Language'),
                        ]
                      )
                    ),
                  ]
                ),
                Expanded( // Expanded를 Row의 직접적인 자식으로 이동
                  child: Container(
                    alignment: Alignment.center,
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: <Widget>[
                          Icon(
                            Icons.mic,
                            size: iconSizeLarge,
                            fill: 1,
                          ),
                        Text(
                          'Test'
                        )
                      ],
                    ),
                  ),
                ),
                Column( //punctuation fix and other fn
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: <Widget>[
                    ElevatedButton(
                      onPressed: () {
                      },
                      style: ElevatedButton.styleFrom(
                        minimumSize: btnDefault, // 버튼의 최소 크기를 200x50으로 설정
                      ),
                      child: Text('Auto Fix'),
                    ),
                    SizedBox(width: pdBtn, height: pdBtn), // 버튼 사이의 간격
                    ElevatedButton(
                      onPressed: () {
                      },
                      style: ElevatedButton.styleFrom(
                        minimumSize: btnDefault, // 버튼의 최소 크기를 200x50으로 설정
                      ),
                      child: Text('Discard'),
                    ),
                    SizedBox(width: pdBtn, height: pdBtn), // 버튼 사이의 간격
                    ElevatedButton(
                      onPressed: () {
                      },
                      style: ElevatedButton.styleFrom(
                        minimumSize: btnDefault, // 버튼의 최소 크기를 200x50으로 설정
                      ),
                      child: Text('Type'),
                    ),
                  ]
                ),
                SizedBox(width: pdWinBorder)
              ],
            ),
          ],
        ),
      ),
    );
  }
}
