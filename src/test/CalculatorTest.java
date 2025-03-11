Here are some test cases for the `Calculator` class in Java:

```java
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertThrows;

public class CalculatorTest {

    @Test
    public void testAdd() {
        Calculator calculator = new Calculator();
        int result = calculator.add(5, 3);
        assertEquals(8, result);
    }

    @Test
    public void testSubtract() {
        Calculator calculator = new Calculator();
        int result = calculator.subtract(10, 4);
        assertEquals(6, result);
    }

    @Test
    public void testMultiply() {
        Calculator calculator = new Calculator();
        int result = calculator.multiply(7, 2);
        assertEquals(14, result);
    }

    @Test
    public void testDivideByZero() {
        Calculator calculator = new Calculator();
        ArithmeticException exception = assertThrows(ArithmeticException.class, () -> calculator.divide(10, 0));
        assertEquals("Cannot divide by zero", exception.getMessage());
    }

    @Test
    public void testDividePositiveNumbers() {
        Calculator calculator = new Calculator();
        int result = calculator.divide(8, 2);
        assertEquals(4, result);
    }

    @Test
    public void testDivideNegativeNumbers() {
        Calculator calculator = new Calculator();
        int result = calculator.divide(-10, -3);
        assertEquals(3, result);
    }
}
```

In these tests:

1. `testAdd`, `testSubtract`, and `testMultiply` test the basic functionality of each method with positive integers.

2. `testDivideByZero` tests that the `divide` method throws an `ArithmeticException` when dividing by zero, as expected.

3. `testDividePositiveNumbers` and `testDivideNegativeNumbers` test the `divide` method with both positive and negative numbers to ensure it works correctly for all cases.

Note: You need to have JUnit library in your project to run these tests.