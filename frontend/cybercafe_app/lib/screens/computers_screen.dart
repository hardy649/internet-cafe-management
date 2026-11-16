
import 'package:flutter/material.dart';
import '../models/computer.dart';
import '../services/api_service.dart';

class ComputersScreen extends StatefulWidget {
  const ComputersScreen({super.key});

  @override
  State<ComputersScreen> createState() => _ComputersScreenState();
}

class _ComputersScreenState extends State<ComputersScreen> {
  late Future<List<Computer>> computers;

  String searchQuery = '';
  String selectedType = 'All';

  @override
  void initState() {
    super.initState();
    computers = ApiService.getComputers();
  }

  void refreshComputers() {
    setState(() {
      computers = ApiService.getComputers();
    });
  }

  String statusText(String status) {
    switch (status) {
      case 'available':
        return 'Сул';
      case 'occupied':
        return 'Завгүй';
      case 'maintenance':
        return 'Засвартай';
      default:
        return status;
    }
  }

  Color statusColor(String status) {
    switch (status) {
      case 'available':
        return Colors.green;
      case 'occupied':
        return Colors.red;
      default:
        return Colors.orange;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('CyberCafe - Computers'),
        backgroundColor: Colors.deepPurple,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            onPressed: refreshComputers,
            icon: const Icon(Icons.refresh),
          ),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: TextField(
              decoration: InputDecoration(
                hintText: 'Компьютерийн нэрээр хайх...',
                prefixIcon: const Icon(Icons.search),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              onChanged: (value) {
                setState(() {
                  searchQuery = value.toLowerCase();
                });
              },
            ),
          ),

          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Row(
              children: ['All', 'Hall', 'VIP', 'Stage']
                  .map((type) {
                return Padding(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 5,
                  ),
                  child: ChoiceChip(
                    label: Text(type),
                    selected: selectedType == type,
                    onSelected: (_) {
                      setState(() {
                        selectedType = type;
                      });
                    },
                  ),
                );
              }).toList(),
            ),
          ),

          const SizedBox(height: 12),

          Expanded(
            child: FutureBuilder<List<Computer>>(
              future: computers,
              builder: (context, snapshot) {
                if (snapshot.connectionState ==
                    ConnectionState.waiting) {
                  return const Center(
                    child: CircularProgressIndicator(),
                  );
                }

                if (snapshot.hasError) {
                  return Center(
                    child: Text('Алдаа: ${snapshot.error}'),
                  );
                }

                final allComputers = snapshot.data ?? [];

                final filtered = allComputers.where((pc) {
                  final matchesName = pc.name
                      .toLowerCase()
                      .contains(searchQuery);

                  final matchesType =
                      selectedType == 'All' ||
                      pc.computerType == selectedType;

                  return matchesName && matchesType;
                }).toList();

                if (filtered.isEmpty) {
                  return const Center(
                    child: Text('Компьютер олдсонгүй'),
                  );
                }

                return ListView.builder(
                  itemCount: filtered.length,
                  itemBuilder: (context, index) {
                    final pc = filtered[index];

                    return Card(
                      margin: const EdgeInsets.symmetric(
                        horizontal: 12,
                        vertical: 6,
                      ),
                      child: ListTile(
                        leading: const Icon(
                          Icons.computer,
                          color: Colors.deepPurple,
                          size: 36,
                        ),
                        title: Text(
                          pc.name,
                          style: const TextStyle(
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        subtitle: Text(
                          'Төрөл: ${pc.computerType}\n'
                          'Үнэ: ${pc.pricePerHour?.toStringAsFixed(0) ?? "Тодорхойгүй"}₮/цаг\n'
                          'Төлөв: ${statusText(pc.status)}',
                        ),
                        isThreeLine: true,
                        trailing: Icon(
                          Icons.circle,
                          color: statusColor(pc.status),
                          size: 15,
                        ),
                      ),
                    );
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
