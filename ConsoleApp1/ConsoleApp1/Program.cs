namespace ConsoleApp1;

class Program
{
    static void Main(string[] args)
    {
        var sol = new Solution();


        var l1 = new ListNode(9);
        
        var l2 = new ListNode(9);
        l2 = l2.next = new ListNode(9);
        l2 = l2.next = new ListNode(9);
        l2 = l2.next = new ListNode(9);

        
        var node = sol.AddTwoNumbers(l1,l2);
        while (node != null)
        {
            Console.WriteLine(node.val);
            node = node.next;
        }
    }
}


public class Solution {
    public ListNode AddTwoNumbers(ListNode l1, ListNode l2)
    {
        int o = 0;

        var list1 = l1;
        var list2 = l2;
        ListNode firstNode = GetNextNode(list1, list2,o, out o);



        var nextNode = firstNode;
        while (list1.next != null)
        {
            list1 = list1.next;
            list2 = list2?.next;
            nextNode.next = GetNextNode(list1, list2, o, out o);    
            //Console.WriteLine(nextNode.next.val);
            nextNode = nextNode.next;
        }
        
        return firstNode;
    }

    static ListNode GetNextNode(ListNode l1, ListNode l2, int add, out int next)
    {
        var v1 = GetVal(l1);
        var v2 = GetVal(l2);

        int n = v1 + v2 + add;
        int r = n % 10;
        next = 0;
        if (n > 9)
        {
            next = 1;
        }
        //Console.WriteLine(r);
        return new ListNode(r);
    }

    private static int GetVal(ListNode l1)
    {
        return l1 != null ? l1.val : 0;
    }
}


public class Solution1
{
    public ListNode AddTwoNumbers(ListNode l1, ListNode l2)
    {
        int next = 0;

        var list1 = l1;
        var list2 = l2;
        ListNode firstNode = GetNextNode(list1, list2, next, out next);
        var nextNode = firstNode;

        while (list1.next != null || list2?.next != null)
        {
            list1 = list1.next;
            list2 = list2?.next;
            nextNode.next = GetNextNode(list1, list2, next, out next);
            nextNode = nextNode.next;
        }

        if (next > 0)
        {
            nextNode.next = new ListNode(next);
        }

        return firstNode;
    }

    static ListNode GetNextNode(ListNode l1, ListNode l2, int add, out int next)
    {
        var v1 = GetVal(l1);
        var v2 = GetVal(l2);

        int sum = v1 + v2 + add;
        next = sum / 10;
        return new ListNode(sum % 10);
    }

    private static int GetVal(ListNode l)
    {
        return l != null ? l.val : 0;
    }
}


 public class ListNode
 {
     public int val;
     public ListNode next;
     public ListNode(int val=0, ListNode next=null) {
         this.val = val;
         this.next = next;
     }
}