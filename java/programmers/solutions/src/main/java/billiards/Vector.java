package billiards;

public class Vector {
  public int x;
  public int y;

  public Vector(int x, int y) {
    this.x = x;
    this.y = y;
  }

  public int squaredNorm() {
    return this.x * this.x + this.y * this.y;
  }
}
