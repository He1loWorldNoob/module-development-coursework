using CRUD.Data;

namespace CRUD.Services;

public class BooksService : IService
{
    private List<Book> _books = new();
    public int BooksCount => _books.Count;
    public void Init()
    {
        //Чтение файла
        //  дозаполнение нехватающих данных
    }

    public void CreateBook()
    {
        Console.Write("Название книги: ");
        string title = Console.ReadLine();
        
        Console.Write("Фио автора: ");
        string autor = Console.ReadLine();
        
        Console.Write("Жанр: ");
        string genre = Console.ReadLine();
        
        Console.Write("Дата написания: ");
        string date = Console.ReadLine();
        
        var book = new Book(title, autor, genre, date);
        _books.Add(book);
        Console.WriteLine();
        Console.WriteLine("-----------------");
        Console.WriteLine("  Книга создана  ");
        Console.WriteLine("-----------------");
        Console.WriteLine(book);
        Console.WriteLine("-----------------");
        
        
    }

    public void RemoveBook(int bookId)
    {
        _books.RemoveAt(bookId);        
    }
}

public class Book
{
    public string Title;
    public string AuthorName;
    public string Date;
    public string Genre;

    public Book(string title, string authorName, string date, string genre)
    {
        Title = title;
        AuthorName = authorName;
        Date = date;
        Genre = genre;
    }

    public override string ToString()
    {
        return $"Название: {Title}\n" +
               $"Автор: {AuthorName}\n" +
               $"Дата: {Date}\n" +
               $"Жанр: {Genre}";
    }
}