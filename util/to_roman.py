def to_roman(num):
  romans = [(5, "V"),(4, "IV"),(1, "I"),]
  result = ""
  for value, symbol in romans:
    while num >= value:
        result += symbol
        num -= value
  return result