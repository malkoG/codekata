package billiards;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;
import static org.assertj.core.api.Assertions.assertThat;

class BilliardTest {
  @Test
  void testHelloWorld() {
    assertThat(helloworld()).isEqualTo("Hello world");
  }

  private String helloworld() {
    return "Hello world";
  }
}
