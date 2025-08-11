// Extracted content of true_string_unordered.cpp

#include <iostream>
#include <string>

class TrueString {
public:
    TrueString(std::string str) : value(str) {}
    std::string getValue() const { return value; }

private:
    std::string value;
};

int main() {
    TrueString ts("Hello, World!");
    std::cout << ts.getValue() << std::endl;
    return 0;
}