namespace ArithmeticFromScratch;

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine(BaseMath.Add(5,5));
        Console.WriteLine(BaseMath.Subtract(5,3));
        Console.WriteLine(BaseMath.Multiply(5,3));
        Console.WriteLine(BaseMath.Divide(15,3));
    }
}


public static class BaseMath
{
    public static int Add(int x, int y) => x + y;
    public static int Subtract( int x, int y) => Add(x, -y);
    public static int Next(int x) => Add(x, 1);
    public static int Back(int x) => Subtract(x, 1);
    
    public static int Multiply(int x, int y)
    {
        var result = 0;
        for (int i = 0; i < y; i = Next(i))
        {
            result += x;    
        }
        return result;
    }

    public static int Divide(int x, int y)
    {
        if (y == 0)
            throw new DivideByZeroException();

        int result = 0;
        int remainder = x;

        while (remainder >= y)
        {
            remainder = Subtract(remainder, y);
            result = Next(result);
        }

        return result;
    }
}
