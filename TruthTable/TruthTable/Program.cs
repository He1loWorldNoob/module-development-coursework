namespace TruthTable;

public static class Program
{
    private static readonly Dictionary<string, Func<bool, bool, bool>> Rules = new()
    {
        ["AND"] = (a, b) => a && b,
        ["OR"] = (a, b) => a || b,
    };
    
    
    static void Main(string[] args)
    {
        AllOperations();
        OperationNot();
    }



    private static void OperationNot()
    {
        Console.WriteLine();
        Console.WriteLine("операция | Операнд | Результат");
        Console.WriteLine("------------------------------");
        for (int i = 1; i >= 0; i--)
        {
            bool o1 = Convert.ToBoolean(i);
            int r = Convert.ToInt32(!o1);

            Console.WriteLine($"   NOT   |    {i}    |     {r}    ");
        }
    }
    
    private static void AllOperations()
    {
        foreach (var rule in Rules)
        {
            WriteOperation(rule.Key);
        }


    }
    
    
    private static void WriteOperation(string op)
    {
        if (!Rules.ContainsKey(op)) return;

        Console.WriteLine();
        Console.WriteLine("Операнд 1 | операция | Операнд 2 | Результат");
        Console.WriteLine("--------------------------------------------");

        for (int i = 1; i >= 0; i--)
        {
            for (int ii = 1; ii >= 0; ii--)
            {
                bool o1 = Convert.ToBoolean(i);
                bool o2 = Convert.ToBoolean(ii);
                int r = Convert.ToInt32(Rules[op](o1, o2));
                Console.WriteLine($"    {i}     |    {op}   |     {ii}     |     {r}    ");
            }
        }
    }

    
    
    
    
}