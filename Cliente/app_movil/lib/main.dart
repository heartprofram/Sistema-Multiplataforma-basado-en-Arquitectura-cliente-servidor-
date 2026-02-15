import 'package:flutter/material.dart';
import 'screens/login_screen.dart';

import 'constants.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'SIGEP App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: kNavyBlue,
          primary: kNavyBlue,
          secondary: kNavyBlue,
        ),
        useMaterial3: true,
      ),
      home: LoginScreen(),
    );
  }
}
