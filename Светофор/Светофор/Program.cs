namespace Светофор;

class Program
{
    private static ConsoleColor[] _colors =
    [
        ConsoleColor.Red,
        ConsoleColor.Yellow,
        ConsoleColor.Green
    ];
    static void Main(string[] args)
    {
        int counter = 0;
        while (true)
        {
            
            int colorId = counter%_colors.Length;

            Console.WriteLine("+-+");
            for (int i = 0; i < _colors.Length; i++)
            {
                DrawLamp(i == colorId ? _colors[i] : ConsoleColor.White);
            }
            Console.WriteLine("+-+   |--|");
            Console.WriteLine(" |    |  |");
            Console.WriteLine(" |    |__|");
            
            
            Console.ReadKey();
            Console.Clear();
            counter++;
            
        }
        
        
    }

    private static void DrawLamp(ConsoleColor color)
    {
        Console.Write("|");
        Console.ForegroundColor = color;
        Console.Write("0");
        Console.ForegroundColor = ConsoleColor.White;
        Console.WriteLine("|");
    }
}
