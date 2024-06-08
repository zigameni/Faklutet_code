### Zadatak 1. (sep14k3-1)

<div align="justify">

Dat je neki sekvencijalni, blokovski orijentisani ulazni uređaj sa koga se blok znakova veličine `BlockSize` učitava na zadatu adresu funkcijom:
```cpp
void readBlock(char* addr);
```
Od ovog uređaja napraviti apstrakciju sekvencijalnog, znakovno orijentisanog ulaznog uređaja (ulazni tok), odnosno realizovati funkciju koja učitava znak po znak sa tog uređaja:


```cpp
char getchar();
```
Ignorisati sve greške.

### Resenje
    Ulazni uredjaj
    - sekvencialni
    - blokovski orjentisan


```cpp

void getChar(){
    static char* blockInput;
    static int cursor=BlockSize;

    if(cursor == BlockSize){
        readBlock(blockInput);
        cursor = 0; 
    }
    return blockInput[cursor];
}

```

</div>
