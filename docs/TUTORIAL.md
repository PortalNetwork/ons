# Tutorial

## Install

Clone the source code and install dependency
```
$ go get github.com/ontio/ontology
$ cd $GOPATH/src/github.com/ontio/ontology
$ glide install
```

Make source code
```
$ make all
```

## Create wallet

```
Yungde-MacBook-Pro-2:ontology phyrex$  ./ontology account add -d
Use default setting '-t ecdsa -b 256 -s SHA256withECDSA'
	signature algorithm: ecdsa
	curve: P-256
	signature scheme: SHA256withECDSA
Password:
Re-enter Password:
Index:2
Label:
Address:AbfNqEyvZJuNzguXTSP6sbioySZpsdYfeY
Public key:03ed07576c4d745edc6dd8938fc7cd24301523d6f95f71c4fc6b283c7184bffcfd
Signature scheme:SHA256withECDSA
Create account successfully.
```

![wallet](../assets/wallet.png)

## Start testnet
```
./ontology --networkid 2
```

![start](../assets/ontology.png)

## Smart Contract

Using smartx
- [https://smartx.ont.io/](https://smartx.ont.io/)

Smart Contract Language
- C#
- Python
- JavaScript (Coming soon)

#### Choosing smartx language
![language](../assets/language.png)

#### Choosing a smartx template, using "Domain"
![smartx-1](../assets/smartx-1.png)

#### Source code
![smartx-2](../assets/smartx-2.png)

#### Compile smartx
![smartx-3](../assets/smartx-3.png)