import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'package:http/http.dart' as http;
import 'package:open_filex/open_filex.dart';
import 'package:path_provider/path_provider.dart';

const String apiBaseUrl = String.fromEnvironment('API_BASE_URL', defaultValue: 'http://localhost:8000');

void main() {
  runApp(const ColoringApp());
}

class ThemeOption {
  final String label;
  final IconData icon;
  ThemeOption(this.label, this.icon);
}

class ColoringApp extends StatelessWidget {
  const ColoringApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Coloring Pages',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
        useMaterial3: true,
      ),
      home: const GeneratorScreen(),
    );
  }
}

class GeneratorScreen extends StatefulWidget {
  const GeneratorScreen({super.key});

  @override
  State<GeneratorScreen> createState() => _GeneratorScreenState();
}

class _GeneratorScreenState extends State<GeneratorScreen> {
  final List<ThemeOption> themes = [
    ThemeOption('animals', Icons.pets),
    ThemeOption('vehicles', Icons.directions_car),
    ThemeOption('fantasy', Icons.auto_fix_high),
    ThemeOption('alphabet', Icons.text_fields),
  ];

  final List<String> ageGroups = ['3-4', '5-6', '7-8'];

  String selectedTheme = 'animals';
  String selectedAge = '3-4';
  bool isLoading = false;
  String? previewBase64;
  String? pdfBase64;
  String? pdfUrl;
  String statusMessage = 'Pick a theme and age to start.';

  Future<void> _generate() async {
    setState(() {
      isLoading = true;
      statusMessage = 'Generating coloring page...';
    });

    try {
      final response = await http
          .post(
            Uri.parse('$apiBaseUrl/generate'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({'theme': selectedTheme, 'age_group': selectedAge}),
          )
          .timeout(const Duration(seconds: 60));

      if (response.statusCode != 200) {
        throw HttpException('Failed: ${response.body}');
      }

      final payload = jsonDecode(response.body) as Map<String, dynamic>;
      if (payload['status'] != 'ok') {
        throw HttpException('Request failed');
      }
      setState(() {
        previewBase64 = payload['preview_base64'] as String?;
        pdfBase64 = payload['pdf_base64'] as String?;
        pdfUrl = payload['pdf_url'] as String?;
        statusMessage = payload['message'] as String? ?? 'Ready to download';
      });
    } catch (err) {
      setState(() {
        statusMessage = 'Error: $err';
      });
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  Future<void> _downloadPdf() async {
    List<int>? bytes;
    if (pdfBase64 != null) {
      bytes = base64Decode(pdfBase64!);
    } else if (pdfUrl != null) {
      final resp = await http.get(Uri.parse('$apiBaseUrl$pdfUrl'));
      if (resp.statusCode == 200) {
        bytes = resp.bodyBytes;
      }
    }

    if (bytes == null) return;

    final directory = await getApplicationDocumentsDirectory();
    final file = File('${directory.path}/coloring_page.pdf');
    await file.writeAsBytes(bytes, flush: true);
    await OpenFilex.open(file.path);

    setState(() {
      statusMessage = 'PDF saved to ${file.path}';
    });
  }

  Widget _buildThemeSelector() {
    return Wrap(
      spacing: 12,
      children: themes
          .map(
            (theme) => ChoiceChip(
              label: Text(theme.label.toUpperCase()),
              avatar: Icon(theme.icon),
              selected: selectedTheme == theme.label,
              onSelected: (_) => setState(() => selectedTheme = theme.label),
            ),
          )
          .toList(),
    );
  }

  Widget _buildAgeSelector() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: ageGroups
          .map(
            (age) => ChoiceChip(
              label: Text('Ages $age'),
              selected: selectedAge == age,
              onSelected: (_) => setState(() => selectedAge = age),
            ),
          )
          .toList(),
    );
  }

  Widget _buildPreview() {
    if (isLoading) {
      return const Padding(
        padding: EdgeInsets.all(24.0),
        child: SpinKitFadingCircle(color: Colors.teal, size: 64),
      );
    }

    if (previewBase64 == null) {
      return const Text('Preview will appear here.');
    }

    return Column(
      children: [
        const Text('Preview', style: TextStyle(fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        Container(
          decoration: BoxDecoration(
            border: Border.all(color: Colors.grey.shade300),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Image.memory(base64Decode(previewBase64!), height: 280),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Coloring Pages'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Choose a theme',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            _buildThemeSelector(),
            const SizedBox(height: 16),
            const Text(
              'Select age group',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            _buildAgeSelector(),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: isLoading ? null : _generate,
                icon: const Icon(Icons.auto_awesome),
                label: const Padding(
                  padding: EdgeInsets.all(12.0),
                  child: Text('Generate coloring page'),
                ),
              ),
            ),
            const SizedBox(height: 24),
            Center(child: _buildPreview()),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(child: Text(statusMessage)),
                ElevatedButton.icon(
                  onPressed: (!isLoading && (pdfBase64 != null || pdfUrl != null))
                      ? _downloadPdf
                      : null,
                  icon: const Icon(Icons.download),
                  label: const Text('Download PDF'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
