#include "ns3/core-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/network-module.h"
#include "ns3/applications-module.h"
#include "ns3/mobility-module.h"
#include "ns3/csma-module.h"
#include "ns3/internet-module.h"
#include "ns3/netanim-module.h"
#include "ns3/wifi-module.h"
#include "ns3/flow-monitor-module.h"

#include "ns3/config-store-module.h"
#include <fstream>

using namespace ns3;
NS_LOG_COMPONENT_DEFINE ("cvicenie 2");

static void GenerateTraffic (Ptr<Socket> socket, uint32_t pktCount, Time pktInterval ){
  if (pktCount > 0)
    {
      std::ostringstream sprava;
      sprava << "Ahoj 1 "<< pktCount << '\0';
      Ptr<Packet> p = Create<Packet> ( (uint8_t*)sprava.str().c_str(), (uint16_t) sprava.str().length() + 1 );
      socket->Send (p);

      Simulator::Schedule (pktInterval, &GenerateTraffic,
                           socket, pktCount-1, pktInterval);
    }
  else
    {
      socket->Close ();
    }
}


int main (int argc, char *argv[]) {
   uint32_t mCsma = 3;
   uint32_t nWifi = 3;
   uint32_t dataSize = 1024;
   bool tra = false, configure=false, app2=true;
   char anim_name[25] = "anim.xml";
   uint32_t pocet_vyslani=3;
   double trvanie=4.;
   double delay=100.0, app2Start=3.0;


   CommandLine cmd;
   cmd.AddValue ("m", "Pocet serverov", mCsma);
   cmd.AddValue ("n", "Pocet wifi stanic.", nWifi);
   cmd.AddValue ("trvanie", "Velkost udajov s sek.", trvanie);

   cmd.AddValue ("A1A2", "Povol aplikaciu 2 Echo al. PacketSend", app2);

   cmd.AddValue ("opak", "Pocet opakovani poslania.", pocet_vyslani);
   cmd.AddValue ("medzi", "Cas medzi posielaniami milisek.", delay);


   cmd.AddValue ("start", "Start aplikacie 2 Echo/koniec=trvanie-0.1s", app2Start);
   cmd.AddValue ("Size", "Velkost echo balika udajov.", dataSize);

   cmd.AddValue ("t", "Povol zapisovanie tcpdump", tra);
   cmd.AddValue ("con", "Povol nacitanie/zapis konfiguracie", configure);
   cmd.AddValue ("anim", "meno anim xml", anim_name);
   cmd.Parse (argc,argv);

// L1
  NodeContainer nW,nP,nS;
  nW.Create (nWifi);//AP+mobily
  nP.Create(2);//R1-R2
  Names::Add ("R2", nP.Get(1));//AP
  Names::Add ("R1", nP.Get(0));
//  for () ... Names::Add ("SrcNode", src);
  nS.Add(nP.Get(1));//R2
  nS.Create(mCsma);//R2+servers
  Names::Add ("PCs", nS.Get(mCsma));
  
  MobilityHelper mobility;
  mobility.SetPositionAllocator ("ns3::RandomBoxPositionAllocator"
                                 ,"X", StringValue("ns3::UniformRandomVariable[Min=0.0|Max=50.0]")
                                 ,"Y", StringValue("ns3::UniformRandomVariable[Min=0.0|Max=50.0]")
                                 ,"Z", StringValue("ns3::ConstantRandomVariable[Constant=1.0]")
  );
  /*mobility.SetPositionAllocator ("ns3::GridPositionAllocator",
                                  "MinX", DoubleValue (0.0),
                                  "MinY", DoubleValue (0.0),
                                  "DeltaX", DoubleValue (5.0),
                                  "DeltaY", DoubleValue (10.0),
                                  "GridWidth", UintegerValue (3),
                                  "LayoutType", StringValue ("RowFirst"));*/
  mobility.SetMobilityModel ("ns3::RandomWalk2dMobilityModel",
                             "Bounds", RectangleValue (Rectangle (0, 50, 0, 50)));
  mobility.Install (nW);

  mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
  mobility.Install (nP.Get(0));//"R1 - AP" nutne
  //dalsie nie su nutne
  //mobility.Install ("R2");
  mobility.SetPositionAllocator ("ns3::GridPositionAllocator"
      , "GridWidth", UintegerValue (1)
      , "MinX", DoubleValue (-10.0)
      , "MinY", DoubleValue (-10.0)
      , "DeltaY", DoubleValue (-7.0)
      );
  mobility.Install(nS);//servery + R2
  
// L2 -- nastavenia NIC a kanalov
  PointToPointHelper p2p; //ADSL linka R1- R2
  p2p.SetDeviceAttribute ("DataRate", StringValue ("5Mbps"));
  p2p.SetChannelAttribute ("Delay", StringValue ("5ms"));
  NetDeviceContainer nicP;
  nicP = p2p.Install (nP);
  
  CsmaHelper csma; // NIC pre servery a R2
  NetDeviceContainer nicS;
  csma.SetChannelAttribute ("DataRate", StringValue ("1000Mbps"));
  csma.SetChannelAttribute ("Delay", TimeValue (MicroSeconds (5)));
  nicS = csma.Install (nS);
  
  YansWifiChannelHelper wChannel = YansWifiChannelHelper::Default();
  YansWifiPhyHelper phy; // MAC
  phy.SetChannel (wChannel.Create ());
  WifiHelper wifi;
  wifi.SetRemoteStationManager ("ns3::AarfWifiManager");
  WifiMacHelper mac;
  Ssid ssid = Ssid ("eduroam");
  mac.SetType ("ns3::StaWifiMac",
               "Ssid", SsidValue (ssid),
               "ActiveProbing", BooleanValue (false));
  NetDeviceContainer nicW;
  nicW = wifi.Install (phy, mac, nW); // mobily NIC
  mac.SetType ("ns3::ApWifiMac"
               //,"Ssid", SsidValue (ssid)
               );
  NetDeviceContainer nicWap;
  nicWap = wifi.Install (phy, mac, nP.Get(0));//R1

// L3 -- IP
    
  InternetStackHelper stack;
  stack.InstallAll();

  Ipv4AddressHelper address;

  address.SetBase ("10.2.1.0", "255.255.255.0");// Ipv4Mask(0xffffff00)); Ipv4Mask ("/24")
  Ipv4InterfaceContainer networkSContainer = address.Assign (nicS);
  address.SetBase ("10.2.4.0", Ipv4Mask ("/30"));
  Ipv4InterfaceContainer networkPContainer = address.Assign (nicP);
  address.SetBase ("10.1.0.0", Ipv4Mask("255.255.0.0"));
  Ipv4InterfaceContainer networkWContainer = address.Assign (nicW);
  address.Assign (nicWap);

  Ipv4GlobalRoutingHelper::PopulateRoutingTables(); // L3
   
//L4-L7
  UdpEchoServerHelper echoServer (9);

  ApplicationContainer serverApps = echoServer.Install ( "PCs") ;
  serverApps.Start (Seconds (1.0));
  serverApps.Stop (Seconds (trvanie));

  Ptr<Node> src = nW.Get(0);
  Ptr<Node> dst = nS.Get(mCsma);
  NS_LOG_UNCOND(dst->GetDevice(1)->GetAddress());

  auto dstIp = dst->GetObject<Ipv4>();
  NS_LOG_UNCOND(dstIp->GetAddress(1,0).GetLocal());
  //networkSContainer.GetAddress(mCsma)
  UdpEchoClientHelper echoClient (dstIp->GetAddress(1,0).GetLocal(), 9);//mCsma=nS.GetN()-1
  echoClient.SetAttribute ("MaxPackets", UintegerValue (pocet_vyslani));
  echoClient.SetAttribute ("Interval", TimeValue (MilliSeconds (delay)));
  echoClient.SetAttribute ("PacketSize", UintegerValue (dataSize));

  ApplicationContainer clientApps = echoClient.Install (src);
  if(app2){
    clientApps.Start (Seconds (app2Start));
    clientApps.Stop (Seconds (trvanie-0.1));
  }


  PacketSinkHelper sinkHelper ("ns3::UdpSocketFactory", InetSocketAddress (dstIp->GetAddress(1,0).GetLocal(), 80));
  TypeId tid = TypeId::LookupByName ("ns3::UdpSocketFactory");
  /*  Ptr<Socket> recvSink = Socket::CreateSocket (dst, tid);
  InetSocketAddress local = InetSocketAddress (dstIp->GetAddress(1,0).GetLocal(), 80);
  recvSink->Bind (local);*/
  Ptr<Socket> source = Socket::CreateSocket (nW.Get(2), tid);
  InetSocketAddress remote = InetSocketAddress (dstIp->GetAddress(1,0).GetLocal(), 80);
  source->Connect (remote);
  ApplicationContainer sinkApp = sinkHelper.Install (dst);


  if(!app2){  Simulator::Schedule (Seconds(app2Start), &GenerateTraffic, source, pocet_vyslani, MilliSeconds(delay));}



  Simulator::Stop (Seconds (trvanie));
  
  //LogComponentEnable ("UdpEchoClientApplication", LOG_LEVEL_INFO);
  //LogComponentEnable ("UdpEchoServerApplication", LOG_LEVEL_INFO);
  if (tra){
      //csma.EnablePcap("ttt",nicS, true);
      phy.EnablePcap("sss",nicW, true);}

  AnimationInterface aml(anim_name);
  aml.EnablePacketMetadata();
  aml.SetMaxPktsPerTraceFile(10000000);// default 100 000packets per trace file
  aml.SetConstantPosition(nP.Get(0), 0,0);
  aml.SetConstantPosition(nP.Get(1), -5,-5);
  //auto bezec = aml.AddResource("/home/student/Documents/share/vis/antenna.png");
  //aml.UpdateNodeImage(nP.Get(0)->GetId(),bezec);
  aml.UpdateNodeSize(nP.Get(0)->GetId(),2,2);

  //bezec = aml.AddResource("/home/student/Documents/share/vis/router.png");
  //aml.UpdateNodeImage(nP.Get(1)->GetId(),bezec);
  aml.UpdateNodeSize(nP.Get(1)->GetId(),2,2);

  //bezec = aml.AddResource("/home/student/Documents/share/vis/server.png");
  for (uint32_t i = 1; i < nS.GetN (); ++i){
        aml.UpdateNodeDescription (nS.Get(i), "Server"+std::to_string(i));
        //aml.UpdateNodeImage(nS.Get(i)->GetId(),bezec);
        aml.UpdateNodeSize(nS.Get(i)->GetId(),2,2);
  }
  aml.UpdateNodeDescription(dst, "dst");
  //bezec = aml.AddResource("/home/student/Documents/share/vis/runner.png");
  for (uint32_t i = 0; i < nW.GetN (); ++i){
        aml.UpdateNodeDescription (nW.Get(i), "bez"+std::to_string(i));
        //aml.UpdateNodeImage(nW.Get(i)->GetId(),bezec);
        aml.UpdateNodeSize(nW.Get(i)->GetId(),2,2);
      }
  aml.UpdateNodeDescription(src, "src");

  if (configure) {
      GtkConfigStore g;
      g.ConfigureAttributes();
  }

  FlowMonitorHelper flowmon;
  Ptr<FlowMonitor> monitor = flowmon.InstallAll ();

  Simulator::Run ();

 /* auto sumOfVector = [](const std::vector<uint32_t,allocator<uint32_t>>& v) -> uint32_t
      {uint32_t sum{}; for (const auto& x : v){sum += x;return sum;} };*/

  monitor->CheckForLostPackets ();
  Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier> (flowmon.GetClassifier ());
  FlowMonitor::FlowStatsContainer stats = monitor->GetFlowStats ();
  for (std::map<FlowId, FlowMonitor::FlowStats>::const_iterator i = stats.begin (); i != stats.end (); ++i) {
    Ipv4FlowClassifier::FiveTuple t = classifier->FindFlow (i->first);
    std::cout << "Flow " << i->first - 2 << " (" << t.sourceAddress << " -> " << t.destinationAddress << ")\n";
    std::cout << "  Tx Packets: " << i->second.txPackets << "\n";
    std::cout << "  Rx Packets:   " << i->second.rxPackets << "\n";
    /*vector of packetsDropped ... by reason code: labda sumOfAll */
    //std::cout << "  Dropped:   " << (i->second.packetsDropped.size()) << "\n";
    std::cout << "  Packet Lost: " << i->second.lostPackets << "\n";
    std::cout << "  Forwarded:   " << i->second.timesForwarded << "\n";
    std::cout << "  DelaySum: " << i->second.delaySum.GetMilliSeconds()  << " ms\n";
    }

  Simulator::Destroy ();
  return 0;
}
