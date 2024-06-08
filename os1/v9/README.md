# Operativni sistemi 1
## Vežbe 9
### Interfejs i implementacija U-I podsistema 1. deo

Lista predmeta:  
[ir2os1@lists.etf.rs](mailto:ir2os1@lists.etf.rs)

#### Interfejs i implementacija U-I podsistema 1. deo

- [x] Zadatak 1. (sep14k3-1)
- [x] Zadatak 2. (sep16k3-1)
- [x] Zadatak 3. (jun14k3-1)
- [x] Zadatak 4. (jun15k3-1)
- [x] Zadatak 5. (jun2019k1-1)
- [x] Zadatak 6. (jun2012k1-1)
- [ ] Zadatak 7. (sep14k1-1)
- [ ] Zadatak 8. (apr14k1-1)
- [ ] Zadatak 9. (sep15k1-1)

---



### Zadatak 2. (sep16k3-1)

Dat je proceduralni interfejs prema nekom blokovski orijentisanom ulaznom uređaju sa direktnim pristupom:
```cpp
extern const int BlockSize;
extern int BlockIOHandle;
long getSize(BlockIOHandle handle);
int readBlock(BlockIOHandle handle, long blockNo, char* addr);
```
Uređaj se identifikuje „ručkom“ tipa `BlockIOHandle`, a blok je veličine `BlockSize` znakova. Operacija `getSize` vraća ukupnu veličinu sadržaja (podataka) na uređaju (u znakovima), a operacija `readBlock` učitava blok sa zadatim brojem u bafer na zadatoj adresi u memoriji i vraća 0 u slučaju uspeha. Obe operacije vraćaju negativnu vrednost u slučaju greške, uključujući i pokušaj čitanja bloka preko granice veličine sadržaja.

Korišćenjem ovog interfejsa implementirati sledeći objektno orijentisani interfejs prema ovom uređaju, koji od njega čini apstrakciju ulaznog toka, odnosno znakovno orijentisanog ulaznog uređaja sa direktnim pristupom:
```cpp
class IOStream {
public:
    IOStream(BlockIOHandle d);
    int seek(long offset);
    int getChar(char& c);
};
```
Operacija `seek` postavlja poziciju „kurzora“ za čitanje na zadatu poziciju (pomeraj počev od znaka na poziciji 0), a operacija `getChar` čita sledeći znak sa tekuće pozicije kurzora u izlazni argument `c` i pomera kurzor za jedno mesto unapred. U slučaju bilo kakve greške, uključujući i pomeranje kursora preko veličine sadržaja ili čitanje znaka kada je kursor stigao do kraja sadržaja, operacije treba da vrate negativnu vrednost, a nulu u slučaju uspeha.

```cpp
class IOStream {
public:
    IOStream(BlockIOHandle d) : dev(d), cursor(-1), curBlock(-1) {
        seek(0);
    }
    int seek(long offset);
    int getChar(char& c);
protected:
    int loadBlock(); // Helper; loads the block corresponding to the cursor
private:
    BlockIOHandle dev;
    char buffer[BlockSize];
    long curBlock, cursor;
};
```

```cpp
int IOStream::loadBlock() {
    long blockNo = cursor / BlockSize;
    if (curBlock == blockNo) return 0;
    if (readBlock(dev, blockNo, buffer) < 0) {
        cursor = -1;
        return -1;
    }
    curBlock = blockNo;
    return 0;
}

int IOStream::seek(int offset) {
    cursor = offset;
    if (cursor < 0 || cursor >= getSize(dev)) {
        cursor = -1;
        return -1;
    }
    return 0;
}

int IOStream::getChar(char& c) {
    if (cursor < 0 || cursor >= getSize(dev)) {
        cursor = -1;
        return -1;
    }
    if (loadBlock() < 0)
        return -1;
    c = buffer[(cursor++) % BlockSize];
    return 0;
}
```



### Zadatak 3. (jun14k3-1)

Dat je neki sekvencijalni, znakovno orijentisani ulazni uređaj (ulazni tok) sa koga se znak učitava sledećom funkcijom:
```cpp
char getchar();
```
Od ovog uređaja napraviti apstrakciju sekvencijalnog, blokovski orijentisanog ulaznog uređaja, sa koga se blok veličine `BlockSize` učitava na zadatu adresu funkcijom:
```cpp
void readBlock(char* addr);
```
Ignorisati sve greške.

Rešenje:
```cpp
void readBlock(char* addr) {
    for (int i = 0; i < BlockSize; i++)
        addr[i] = getchar();
}
```

---

### Zadatak 4. (jun15k3-1)

U nekom sistemu svaki drajver blokovski orijentisanog uređaja („diska“) registruje sledeću strukturu (tabelu) koja sadrži pokazivače na funkcije koje implementiraju odgovarajuće operacije sa tim uređajem:
```cpp
typedef ... Byte; // Unit of memory
typedef ... BlkNo; // Disk block number
typedef int (*DiskOperation)(BlkNo block, Byte* buffer);

struct DiskOperationsTable {
    int isValid;
    DiskOperation readBlock, writeBlock;
    DiskOperationsTable() : isValid(0), readBlock(0), writeBlock(0) {}
};
```
Sistem organizuje tabelu registrovanih drajvera za priključene uređaje kao niz ovih struktura, s tim da polje `isValid == 1` označava da je dati element niza zauzet (validan, postavljen, odnosno disk je registrovan), a `0` da je ulaz slobodan (disk nije registrovan):
```cpp
const int MaxNumOfDisks; // Maximal number of registered disk devices
DiskOperationsTable disks[MaxNumOfDisks];
```
Sistem preslikava simbolička imena dodeljena priključenim uređajima, u obliku slova abecede, brojevima ulaza u tabeli `disks` (u opsegu od `0` do `MaxNumOfDisks-1`).

**a) Realizovati funkcije:**
```cpp
int readBlock(int diskNo, BlkNo block, Byte* buffer) {
    if (diskNo < 0 || diskNo >= MaxNumOfDisks) return -1; // Error
    if (disks[diskNo].isValid == 0) return -2; // Error
    if (disks[diskNo].readBlock == 0) return -3; // Error
    return (disks[diskNo].readBlock)(block, buffer);
}

int writeBlock(int diskNo, BlkNo block, Byte* buffer) {
    if (diskNo < 0 || diskNo >= MaxNumOfDisks) return -1; // Error
    if (disks[diskNo].isValid == 0) return -2; // Error
    if (disks[diskNo].writeBlock == 0) return -3; // Error
    return (disks[diskNo].writeBlock)(block, buffer);
}
```

**b) Realizovati funkciju koja registruje operacije drajvera za dati disk:**
```cpp
int registerDriver(int diskNo, DiskOperation read, DiskOperation write) {
    if (diskNo < 0 || diskNo >= MaxNumOfDisks) return -1; // Error
    if (disks[diskNo].isValid) return -2; // Error
    disks[diskNo].isValid = 1;
    disks[diskNo].readBlock = read;
    disks[diskNo].writeBlock = write;
    return 0;
}
```

---

### Zadatak 5. (jun19k1-1)

Date su deklaracije pokazivača preko kojih se može pristupiti registrima dva ulazno/izlazna uređaja:
```cpp
typedef volatile unsigned int REG;

REG* io1Ctrl = ...; // Device 1 control register
REG* io1Status = ...; // Device 1 status register
REG* io1Data = ...; // Device 1 data register
REG* io2Ctrl = ...; // Device 2 control register
REG* io2Status = ...; // Device 2 status register
REG* io2Data = ...; // Device 2 data register
```
U upravljačkim registrima najniži bit je bit `Start` kojim se pokreće uređaj, a u statusnim registrima najniži bit je bit spremnosti (`Ready`). Svi registri su veličine jedne mašinske reči (tip `unsigned int`). Potrebno je napisati funkciju `transfer` koja najpre vrši ulaz bloka podataka zadate veličine sa prvog uređaja korišćenjem tehnike prozivanja (polling), a potom izlaz tog istog učitanog bloka podataka na drugi uređaj korišćenjem prekida, i vraća kontrolu pozivaocu tek kada se oba prenosa završe.

```cpp
static REG* ioPtr = 0;
static int ioCount = 0;
static int ioCompleted = 0;

void transfer(int count) {
    REG* buffer = new REG[count];
    // I/O 1
    ioPtr = buffer;
    ioCount = count;
    *io1Ctrl = 1; // Start I/O 1
    while (ioCount > 0) {
        while (!(*io1Status & 1)); // busy wait
        *ioPtr++ = *io1Data;
        ioCount--;
    }
    *io1Ctrl = 0; // Stop I/O 1
    // I/O 2:
    ioPtr = buffer;
    ioCount = count;
    ioCompleted = 0;
    *io2Ctrl = 1; // Start I/O 2
    while (!ioCompleted); // Wait for I/O 2 completion:
    delete[] buffer;
}

interrupt void io2Interrupt() {
    *io2Data = *ioPtr++;
    if (--ioCount == 0) {
        ioCompleted = 1;
        *io2Ctrl = 0; // Stop I/O 2
    }
}
```

---

### Zadatak 6. (jun12k1-1)

Date su deklaracije pokazivača preko kojih se može pristupiti registrima jednog DMA uređaja:
```cpp
typedef unsigned int REG;

REG* dmaCtrl = ...; // control register
REG* dmaStatus = ...; // status register
REG* dmaBlkAddr = ...; // data block address register
REG* dmaBlkSize = ...; // data block size register
```
U upravljačkom registru najniži bit je bit `Start` kojim se pokreće prenos preko DMA, a u statusnom registru najniži bit je bit spremnosti (`Ready`) čija vrednost `1` ukazuje da je DMA spreman za novi prenos podatka (inicijalno je tako postavljen). Postavljanje bita spremnosti kada DMA završi zadati prenos generiše signal zahteva za prekid procesoru. Zahtevi za izlaznim operacijama na nekom izlaznom uređaju vezani su u jednostruko ulančanu listu. Zahtev ima sledeću strukturu:
```cpp
struct OutputRequest {
    char* buffer; // Buffer with data (block)
    unsigned int size; // Buffer (blok) size
    void (*callBack)(OutputRequest*); // Call-back function
    OutputRequest* next; // Next in the list
};
```
Kada se završi prenos zadat jednim zahtevom, potrebno je pozvati funkciju na koju ukazuje pokazivač `callBack` u tom zahtevu, sa argumentom koji ukazuje na taj zahtev. Ovu funkciju implementira onaj ko je zahtev postavio i služi da mu signalizira da je zahtev obrađen. Obrađeni zahtev ne treba brisati iz liste (to je odgovornost onog ko je zahtev postavio). Potrebno je napisati kod operacije `transfer()`, zajedno sa odgovarajućom prekidnom rutinom `dmaInterrupt()`, koja obavlja sve prenose zadate zahtevima u listi na čiji prvi zapis ukazuje argument `ioHead`.

```cpp
static int dmaCompleted = 0;

void transfer(OutputRequest* ioHead) {
    while (ioHead) {
        dmaCompleted = 0; // initialize transfer
        *dmaBlkAddr = ioHead->buffer;
        *dmaBlkSize = ioHead->size;
        *dmaCtrl = 1; // start transfer
        while (!dmaCompleted); // wait for DMA to complete
        ioHead->callBack(ioHead); // signal completion
        ioHead = ioHead->next; // take next
    }
}

interrupt void dmaInterrupt() {
    dmaCompleted = 1;
}
```

---

### Zadatak 7. (sep14k1-1)

Date su deklaracije pokazivača preko kojih se može pristupiti registrima jednog ulaznog uređaja i registru posebnog uređaja – vremenskog brojača:
```cpp
typedef unsigned int REG;

REG* ioCtrl = ...; // Device control register
REG* ioData = ...; // Device data register
REG* timer = ...; // Timer
```
Učitavanje svakog pojedinačnog podatka sa ovog ulaznog uređaja zahteva se posebnim upisom vrednosti `1` u najniži bit upravljačkog registra ovog uređaja. Spremnost ulaznog podatka u registru za podatke uređaj ne signalizira nikakvim signalom, ali je sigurno da je ulazni podatak spreman u registru podataka najkasnije `50 ms` nakon zadatog zahteva (upisa u kontrolni registar).

Na magistralu računara vezan je i registar posebnog uređaja, vremenskog brojača. Upisom celobrojne vrednosti `n` u ovaj registar, vremenski brojač počinje merenje vremena od `n` ms i, nakon isteka tog vremena, generiše prekid procesoru.

Potrebno je napisati kod operacije `transfer()` zajedno sa odgovarajućom prekidnom rutinom za prekid od vremenskog brojača `timerInterrupt()`, koja obavlja učitavanje bloka podataka zadate dužine na zadatu adresu u memoriji sa datog ulaznog uređaja.
```cpp
void transfer (REG* buffer, unsigned int count);
interrupt void timerInterrupt ();
```
```cpp
static const unsigned int timeout = 50; // 50 ms
static int completed = 0;
static REG* ptr = 0;
static unsigned int count = 0;

void transfer (REG* buffer, unsigned int cnt) {
    // Initialize transfer
    completed = 0;
    ptr = buffer;
    count = cnt;
    // Start transfer:
    *ioCtrl = 1; // Input request
    *timer = timeout; // Start timer
    while (!completed); // Busy wait for transfer completion
}

interrupt void timerInterrupt () {
    *ptr++ = *ioData; // Read data
    if (--count) {
        *ioCtrl = 1; // New input request
        *timer = timeout; // Restart timer
    } else // Completed
        completed = 1;
}
```

---

### Zadatak 8. (apr14k1-1)

Date su deklaracije pokazivača preko kojih se može pristupiti registrima dva DMA kontrolera:
```cpp
typedef unsigned int REG;

REG* dma1Ctrl = ...; // DMA1 control register
REG* dma1Status = ...; // DMA1 status register
REG* dma1Address = ...; // DMA1 block address register
REG* dma1Count = ...; // DMA1 block size register
REG* dma2Ctrl = ...; // DMA2 control register
REG* dma2Status = ...; // DMA2 status register
REG* dma2Address = ...; // DMA2 block address register
REG* dma2Count = ...; // DMA2 block size register
```
U upravljačkom registru najniži bit je bit `Start` kojim se pokreće prenos jednog bloka preko DMA, a u statusnom registru najniži bit je bit završetka prenosa (`TransferComplete`), a bit do njega bit greške (`Error`). Svi registri su veličine jedne mašinske reči (tip `unsigned int`). Kada DMA konotroler završi zadati prenos, on se automatski zaustavlja (nije ga potrebno zaustavljati upisom u upravljački registar). Završetak prenosa sa bilo kog DMA kontrolera generiše isti zahtev za prekid procesoru (signali završetka operacije sa dva DMA kontrolera vezani su na ulazni zahtev za prekid preko OR logičkog kola).

Zahtevi za ulaznim operacijama na nekom uređaju sa kog se prenos blokova vrši preko bilo kog od ova DMA kontrolera vezani su u jednostruko ulančanu listu. Zahtev ima sledeću strukturu:
```cpp
struct IORequest {
    REG* buffer; // Data buffer (block)
    unsigned int size; // Buffer (blok) size
    int status; // Status of operation
    IORequest* next; // Next in the list
};
```
Na prvi zahtev u listi pokazuje globalni pokazivač `ioHead`. Kada kernel u listu stavi novi zahtev, pozvaće operaciju `transfer()` koja treba da pokrene prenos za taj zahtev na bilo kom trenutno slobodnom DMA kontroleru (u slučaju da su oba kontrolera zauzeta ne treba ništa uraditi). Zahtev koji se dodeli nekom od DMA kontrolera na obradu ibacuje se iz liste. Kada se završi prenos zadat jednim zahtevom na jednom DMA kontroleru, potrebno je u polje `status` date strukture preneti status završene operacije (0 – ispravno završeno do kraja, -1 – greška) i pokrenuti prenos za sledeći zapis u listi na tom DMA kontroleru, i potom izbaciti zahtev iz liste. Obratiti pažnju na to da oba DMA kontrolera mogu završiti prenos i generisati prekid istovremeno. Ako zahteva u listi više nema, ne treba uraditi više ništa (kada bude stavljao novi zahtev u listu, kernel će proveriti i videti da je ona bila prazna, pa pozvati ponovo operaciju `transfer()` itd.).

Potrebno je napisati kod operacije `transfer()`, zajedno sa odgovarajućom prekidnom rutinom `dmaInterrupt()` za prekid od DMA kontrolera.
```cpp
void transfer ();
interrupt void dmaInterrupt ();
```
```cpp
IORequest *dma1Pending = 0, *dma2Pending = 0; // Currently pending requests

void startDMA1 () {
    if (ioHead != 0 && dma1Pending == 0) {
        dma1Pending = ioHead; // Take the first request,
        ioHead = ioHead->next; // remove it from the list
        *dma1Address = dma1Pending->buffer; // and assign it to DMA1
        *dma1Count = dma1Pending->size;
        *dma1Ctrl = 1; // Start I/O
    }
}

void startDMA2 () {
    if (ioHead != 0 && dma2Pending == 0) {
        dma2Pending = ioHead; // Take the first request,
        ioHead = ioHead->next; // remove it from the list
        *dma2Address = dma2Pending->buffer; // and assign it to DMA2
        *dma2Count = dma2Pending->size;
        *dma2Ctrl = 1; // Start I/O
    }
}

void transfer () { 
    startDMA1(); 
    startDMA2(); 
}

interrupt void dmaInterrupt () {
    if (dma1Status & 1) { // DMA1 completed
        if (dma1Pending == 0) return; // Exception
        if (*dma1Status & 2) // Error in I/O
            dma1Pending->status = -1;
        else
            dma1Pending->status = 0;
        dma1Pending = 0;
        startDMA1();
    }
    if (dma2Status & 1) { // DMA2 completed
        if (dma2Pending == 0) return; // Exception
        if (*dma2Status & 2) // Error in I/O
            dma2Pending->status = -1;
        else
            dma2Pending->status = 0;
        dma2Pending = 0;
        startDMA2();
    }
}
```
In this code, we have two DMA controllers `dma1` and `dma2`, each with its control, status, address, and count registers. The `transfer()` function is responsible for initiating DMA transfers for pending requests. The `startDMA1()` and `startDMA2()` functions start a DMA transfer if there is a pending request and the respective DMA controller is available. The `dmaInterrupt()` function handles DMA completion interrupts, updating the status of the completed request and initiating the next transfer if there are pending requests in the queue.