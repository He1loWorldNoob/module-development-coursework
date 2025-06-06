using System.Numerics;

namespace PifagorTable;

class Program
{
    static int _indent;

    static void Main(string[] args)
    {
        

        Console.WriteLine("Введите размер таблицы");

        int x = GetInputNum();
        int y = GetInputNum();

        _indent = (x * y + "").Length + 1;
        Console.WriteLine();
        for (int i = 1; i <= x; i++)
        {
            //var line = "";
            for (int ii = 1; ii <= y; ii++)
            {
                int index = i * ii;
                var column = "";
                if (index != 1)
                {
                    column += index;
                }

                if (i == 1 || ii == 1)
                    Console.ForegroundColor = ConsoleColor.Red;
                Console.Write(SetIndent(column));
                Console.ForegroundColor = ConsoleColor.White;

            }
            Console.WriteLine();
        }
    }

    private static int GetInputNum()
    {
        int y;
        while (!GetValidInput(out y))
        {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("Ошибка, введите целое число которое больше 1!");
            Console.ForegroundColor = ConsoleColor.White;
        }

        return y;
    }

    private static bool GetValidInput(out int num)
    {
        var input = Console.ReadLine();
        return int.TryParse(input, out num) && num > 1;
    }

    static string SetIndent(string text)
    {
        string result = text;
        for (int i = text.Length; i < _indent; i++)
        {
            result = " " + result;
        }
        return result;
    }
}