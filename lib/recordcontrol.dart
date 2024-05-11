import 'dart:async';

import 'package:flutter_sound/flutter_sound.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:path_provider';

class SoundRecorder {
  late FlutterSoundRecorder _recorder;
  bool _isRecorderInitialized = false;
  bool isRecording = false; //needed to refered outside the class
  bool isRecordingPaused = false;

  Future<void> init() async {
    _recorder = FlutterSoundRecorder();

    final status = await Permission.microphone.request();
    if (status != PermissionStatus.granted) {
      throw RecordingPermissionException('마이크 권한이 필요합니다.');
    }

    await _recorder.openRecorder();
    _isRecorderInitialized = true;
  }

  Future<void> startRecording() async {
    if (!_isRecorderInitialized) return;
    isRecording = true;
    print("Start recording");
    await _recorder.startRecorder(toFile: 'sample.mp3');
  }

  Future<void> stopRecording() async {
    if (!_isRecorderInitialized) return;
    isRecording = false;
    print("Stop recording");
    await _recorder.stopRecorder();
  }

  Future<void> pauseRecording() async {
    if(isRecording) {
      if(!isRecordingPaused) {
      _recorder.pauseRecorder();
      isRecordingPaused = true;
      }
      else if(isRecordingPaused) {
      _recorder.resumeRecorder();
      isRecordingPaused = false;
      }
    }
  }

  Future<void> dispose() async {
    if (!_isRecorderInitialized) return;
    _recorder.closeRecorder();
    _isRecorderInitialized = false;
  }
}
