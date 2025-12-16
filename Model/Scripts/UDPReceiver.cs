using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;

public class UDPReceiver : MonoBehaviour
{
    UdpClient client;
    public static string data;

    void Start()
    {
        client = new UdpClient(5052);
        client.BeginReceive(Receive, null);
    }

    void Receive(System.IAsyncResult ar)
    {
        IPEndPoint ip = new IPEndPoint(IPAddress.Any, 0);
        byte[] bytes = client.EndReceive(ar, ref ip);
        data = Encoding.UTF8.GetString(bytes);
        client.BeginReceive(Receive, null);
    }
}
