
class Computer {
  final int id;
  final String name;
  final String computerType;
  final String status;
  final String specifications;
  final double? pricePerHour;

  Computer({
    required this.id,
    required this.name,
    required this.computerType,
    required this.status,
    required this.specifications,
    required this.pricePerHour,
  });

  factory Computer.fromJson(Map<String, dynamic> json) {
    return Computer(
      id: json['id'],
      name: json['name'] ?? '',
      computerType: json['computer_type_name'] ?? '',
      status: json['status'] ?? '',
      specifications: json['specifications'] ?? '',
      pricePerHour: double.tryParse(
        json['price_per_hour']?.toString() ?? '',
      ),
    );
  }
}
