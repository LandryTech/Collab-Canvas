from point import Point
print()

# Point A -- A brand new point made from scratch
a = Point(960, 540, 1920, 1080, 5, Point.PINK)
print(f"Point A:")
print(f"toString(): {a.toString()}")
print(f"getWidth(): {a.getWidth()}, getHeight(): {a.getHeight()}, getPosX(): {a.getPosX()}, getPosY(): {a.getPosY()}, getRad(): {a.getRad()}")

# Point B -- A point using the same information as Point A WHILE using the same canvas width and height
print()
b = Point.initialization(a.toStringEncode(), a.getWidth(), a.getHeight())
print(f"Point B:")
print(f"toString(): {b.toString()}")
print(f"getWidth(): {b.getWidth()}, getHeight(): {b.getHeight()}, getPosX(): {b.getPosX()}, getPosY(): {b.getPosY()}, getRad(): {b.getRad()}")

# Point C -- A point using the same information as Point A BUT using a different canvas width and height
print()
c = Point.initialization(a.toStringEncode(), 1440, 900)
print(f"Point C:")
print(f"toString(): {c.toString()}")
print(f"getWidth(): {c.getWidth()}, getHeight(): {c.getHeight()}, getPosX(): {c.getPosX()}, getPosY(): {c.getPosY()}, getRad(): {c.getRad()}")

print()

print(a.toStringEncode())
print(b.toStringEncode())

print()