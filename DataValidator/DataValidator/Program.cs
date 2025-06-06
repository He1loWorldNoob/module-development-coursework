using System.ComponentModel.DataAnnotations;
using System.Net;

namespace DataValidator;

using System.Text.RegularExpressions;

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Номер телефона валидный: " + IsValidTelephoneNumber("+79321139965"));
        Console.WriteLine("ИНН валидный: "  + ValidateInn("667119553352"));
        Console.WriteLine("IPV4 валидный: " + ValidateIpV4("192.168.0.1"));
        Console.WriteLine("IPV6 валидный: " + ValidateIpV6("1050:0000:0000:0000:0005:0600:300c:326b"));
        Console.WriteLine("Guid валидный: " + ValidGuid("3F2504E0-4F89-41D3-9A0C-0305E82C3301"));
        Console.WriteLine("Mail валидный: " + IsValidEmail("ufj1975@ya.ru"));
        Console.WriteLine("Возраст валидный: " + IsAgeValid("21"));
        Console.WriteLine("Карта валидна: " + IsValidCardNumber("2200770645869068"));
        Console.WriteLine("Время валидно: " + IsValidTime("17:00:00"));
        Console.WriteLine("Mac-адрес валиден: " + IsValidMacAddress("D4:5D:64:3C:EA:51"));
    }

    public static bool IsValidMacAddress(string macAddress)
    {
        string pattern = "([0-9a-fA-F]{2}([:-]|$)){6}$|([0-9a-fA-F]{4}([.]|$)){3}";
        return Regex.IsMatch(macAddress, pattern);
    }
    public static bool IsValidCardNumber(string cardNumber)
    {
        string pattern = "[0-9]{16}";
        return Regex.IsMatch(cardNumber, pattern);
    }
    public static bool IsValidTime(string time)
    {
        string pattern = "^([0-1]\\d|2[0-3])(:[0-5]\\d){2}$";
        return Regex.IsMatch(time, pattern);
    }
    public static bool IsAgeValid(string age)
    {
        if(!int.TryParse(age, out int ageInt)) return false;
        return ageInt > 1 && ageInt<100;
    }
    
    public static bool IsValidEmail(string email)
    {
        string regex = "^[-\\w.]+@([A-z0-9][-A-z0-9]+\\.)+[A-z]{2,4}$";

        return Regex.IsMatch(email, regex);
    }
    public static bool ValidateIpV4(string ipV4)
    {
        string regex = "((25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\.){3}(25[0-5]|2[0-4]\\d|[01]?\\d\\d?)";

        return Regex.IsMatch(ipV4, regex);
    }
    
    public static bool ValidateIpV6(string ipV6)
    {
        string regex = "((^|:)([0-9a-fA-F]{0,4})){1,8}$";

        return Regex.IsMatch(ipV6, regex);
    }
    
    public static bool ValidGuid(string guid)
    {
        string regex = "^[0-9A-Fa-f]{8}\\-[0-9A-Fa-f]{4}\\-[0-9A-Fa-f]{4}\\-[0-9A-Fa-f]{4}\\-[0-9A-Fa-f]{12}$";

        return Regex.IsMatch(guid, regex);
    }
    

    //ИНН

    public static bool ValidateInn(string? inn)
    {
        if (string.IsNullOrEmpty(inn))
        {
            Console.WriteLine("ИНН пуст");
            return false;
        }

        if (Regex.IsMatch(inn, "[^0-9]"))
        {
            Console.WriteLine("ИНН может состоять только из цифр");
            return false;
        }

        if (inn.Length != 10 && inn.Length != 12)
        {
            Console.WriteLine("ИНН может состоять только из 10 или 12 цифр");
            return false;
        }

        int CheckDigit(string s, int[] coef)
        {
            int sum = 0;
            for (int i = 0; i < coef.Length; i++)
                sum += coef[i] * int.Parse(s[i].ToString());
            return sum % 11 % 10;
        }

        if (inn.Length == 10)
        {
            var k10 = new[] { 2, 4, 10, 3, 5, 9, 4, 6, 8 };
            int d = CheckDigit(inn, k10);
            return d == int.Parse(inn[9].ToString());
        }
        
        if (inn.Length == 12)
        {
            var k11 = new[] { 7, 2, 4, 10, 3, 5, 9, 4, 6, 8 };
            var k12 = new[] { 3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8 };
            int d1 = CheckDigit(inn, k11);
            int d2 = CheckDigit(inn, k12);
            return d1 == int.Parse(inn[10].ToString()) && d2 == int.Parse(inn[11].ToString());
        }
        Console.WriteLine("Неправильное контрольное число");
        return false;
    }


    public static bool IsValidTelephoneNumber(string telephoneNumber)
    {
        string regexStr = @"^\+7\d{10}$";
        return Regex.IsMatch(telephoneNumber, regexStr);
    }
}