# Computer Networks 2

## History of the Internet

### ARPANET (1969 – 1989)
The ARPANET was the first major packet-switching network, funded by the United States Department of Defense. It connected academic, research, and governmental institutions, making it a non-commercial network. Initially, it used the Network Control Protocol (NCP) but switched to the more robust TCP/IP protocol on January 1, 1983. Email became a key application in 1972. Before the advent of the Domain Name System (DNS) in the early 1980s, a centralized HOSTS.TXT file at Stanford Research Institute listed all hosts, which was not scalable. The routers, known as Interface Message Processors (IMP), utilized distance-vector routing. In 1982, the Exterior Gateway Protocol (EGP) was introduced to manage routing between autonomous systems.

![ARPANET](media/image_arpnet.png)

### NSFNET (1985 - 1995)
NSFNET, funded by the National Science Foundation, aimed to connect academic and research institutions using a hierarchical architecture consisting of a backbone, regional networks, and campus networks. It began with a 56kbps backbone and later upgraded to T1 and T3 speeds. As commercial networks emerged in the early 1990s, there was a need to connect with these networks, leading to the development of similar networks in Europe and Asia, such as JANET in the UK.

### Further Development (1989-1994)
Government networks exchanged traffic via the Federal Internet eXchange (FIX) on the East and West coasts of the US starting in 1989. Commercial networks began using the Commercial Internet eXchange (CIX) in 1991. The first Internet Service Providers (ISPs) appeared, and SPRINT was tasked with connecting NSFNET to European and Asian networks. The Border Gateway Protocol version 4 (BGPv4) was introduced in 1994.

## Modern Internet Organization

The modern Internet no longer relies on a single backbone network but consists of a distributed architecture of interconnected networks operated by various providers and users. Connectivity between providers is measured in thousands, and traffic is exchanged at numerous "exchange points." Large providers have multiple points of presence (PoPs) to connect with users.

### Traffic Exchange Between Networks
Traffic is exchanged via Network Access Points (NAPs) as part of the NSFNET project, or through direct ISP connections. These exchange points are typically non-profit organizations, and almost every country has its own exchange points.

### Routing Arbiter (RA)
Funded by the NSF, the Routing Arbiter project was designed to manage the complexity of forming BGP connections between every provider at large exchange points. Instead, all providers exchange routes and establish BGP connections with the RA.

## Post-NSFNET Initiatives

Several high-speed research and educational networks were developed after NSFNET, including:
- **vBNS (Very high speed Backbone Network Service)** - Established in 1995 as a research network.
- **Internet 2/Abilene**
- **TEN-34**
- **TEN-155**
- **GEANT Series (GN/GEANT, GN2/GEANT2, GN3/GEANT3, GN3+, GN4)** - With GN4 Phase 1 and Phase 2 starting in April 2016.

## Internet Organization by Layers

The Internet is informally divided into three tiers:
- **Tier 1:** Networks (ISPs) that exchange traffic with all other Tier 1 networks, enabling access to all destinations on the Internet.
- **Tier 2:** Networks that exchange traffic with some networks but must purchase IP transit to reach certain destinations.
- **Tier 3:** Networks that exclusively purchase transit to reach all Internet destinations.

### Tier 1 Providers (2008)
Tier 1 ISPs form a closed group with strict peering agreements. Violating these agreements, such as selling Internet services at low prices, can result in exclusion from the Tier 1 group. Disconnection between any two Tier 1 ISPs can effectively split the Internet.

Tier 1 networks in 2008 included:
- AOL Transit Data Network (ATDN) (AS1668)
- AT&T (AS7018)
- Global Crossing (GX) (AS3549)
- Level 3 (AS3356)
- Verizon Business (UUNET) (AS701)
- NTT Communications (Verio) (AS2914)
- Qwest (AS209)
- SAVVIS (AS3561)
- Sprint Nextel Corporation (AS1239)

## Content Distribution on the Internet

Content Delivery Networks (CDNs) are essential for distributing web, multimedia, and live content. They use a distributed architecture to avoid server overloads. Akamai is the largest CDN with 300,000 servers in 136 countries as of October 2020. Other notable CDNs include Limelight, EdgeStream, and Level3.

### Key Entities in CDNs
- **Client:** The end user requesting content.
- **CDN:** Replica servers (content caches) that store copies of content.
- **Content Provider:** The original source of the content.

## Internet Organizations

### Key Organizations

- **ICANN (Internet Corporation for Assigned Names and Numbers):** Established in 1998, ICANN is a non-profit private organization in California, overseeing IP addresses, port numbers, and root DNS servers.
- **IANA (Internet Assigned Numbers Authority):** Established in 1988 by DARPA, IANA manages IP addresses, autonomous system numbers, and port numbers. It operates under ICANN through a contract with the US Department of Commerce.
- **RIR (Regional Internet Registries):** Organizations like RIPE, ARIN, and APNIC manage regional IP address allocation.
- **UN (Internet Governance Forum):** Established in 2006 to discuss public policy issues related to Internet governance.

### Supporting Organizations

- **ISOC (Internet Society):** Founded in 1992 as a private non-profit organization in Reston, VA, ISOC supports Internet standards development, with 130 organizational members and 55,000 individual members.
- **IAB (Internet Architecture Board):** A committee within ISOC that oversees the IETF and IRTF.
- **IETF (Internet Engineering Task Force):** Founded in 1986, IETF develops and promotes voluntary Internet standards, particularly through its working groups and RFC (Request for Comments) documents.
- **IRTF (Internet Research Task Force):** Established in 1989, IRTF focuses on long-term research related to Internet protocols, applications, architecture, and technology.