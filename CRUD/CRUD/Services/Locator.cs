namespace CRUD.Services;

public static class Locator
{
    private static readonly Dictionary<Type, IService> Services = new();
    
    public static T Resolve<T>() where T : class, IService, new()
    {
        if(Services.ContainsKey(typeof(T)))
            return (T)Services[typeof(T)];
        var service = new T();
        Services[typeof(T)] = service;
        return service;
    }
    
}
public interface IService { }