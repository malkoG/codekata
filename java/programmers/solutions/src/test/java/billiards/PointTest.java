package billiards;

import jdk.jfr.Description;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;
import static org.assertj.core.api.Assertions.assertThat;

class PointTest {
  @Test
  @Description("두 좌표 간의 거리는 x 축에서의 거리의 제곱과 y 축에서의 거리의 제곱의 합으로 나타낸다.")
  void testDistance() {
    int[][][] arrayOfCoordinates = {
      {{1, 2}, {3, 4}},
      {{3, 7}, {7, 7}},
      {{3, 7}, {2, 7}},
      {{3, 7}, {7, 3}},
    };

    for (int[][] points : arrayOfCoordinates) {
      Point u = new Point(points[0][0], points[0][1]);
      Point v = new Point(points[1][0], points[1][1]);

      Vector vec = new Vector(u.x - v.x, u.y - v.y);

      assertThat(vec.squaredNorm()).isEqualTo(vec.x * vec.x + vec.y * vec.y);
    }
  }
}
