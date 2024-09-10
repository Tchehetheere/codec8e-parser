#!/usr/bin/python3
import binascii, json, datetime

DATA_BYTE = {
    "START_POS" : 34,
    "IMEI_LEN" : 2,
    "IMEI" : 15,
    "AVL_PREAMBLE_LEN" : 4,
    "AVL_LENGTH_LEN" : 4,
    "AVL_CODEC_ID_LEN" : 1,
    "AVL_NUM_OF_DATA_1_LEN" : 1,
    "AVL_NUM_OF_DATA_2_LEN" : 1,
    "AVL_TIMESTAMP_LEN" : 8,
    "AVL_PRIORITY_LEN" : 1,
    "AVL_LONGITUDE_LEN" : 4,
    "AVL_LATITUDE_LEN" : 4,
    "AVL_ALTITUDE_LEN" : 2,
    "AVL_ANGLE_LEN" : 2,
    "AVL_SATELLITES_LEN" : 1,
    "AVL_SPEED_LEN" : 2,
    "AVL_EVENT_IO_ID_LEN" : 2,
    "AVL_N_TOTAL_IO_LEN" : 2,
    "AVL_N1_TOTAL_IO_LEN" : 2,
    "AVL_N1_IO_ID_LEN" : 2,
    "AVL_N1_IO_VALUE_LEN" : 1,
    "AVL_N2_TOTAL_IO_LEN" : 2,
    "AVL_N2_IO_ID_LEN" : 2,
    "AVL_N2_IO_VALUE_LEN" : 2,
    "AVL_N4_TOTAL_IO_LEN" : 2,
    "AVL_N4_IO_ID_LEN" : 2,
    "AVL_N4_IO_VALUE_LEN" : 4,
    "AVL_N8_TOTAL_IO_LEN" : 2,
    "AVL_N8_IO_ID_LEN" : 2,
    "AVL_N8_IO_VALUE_LEN" : 8,
    "AVL_NX_TOTAL_IO_LEN" : 2,
    "AVL_NX_IO_ID_LEN" : 2,
    "AVL_NX_IO_LENGTH_LEN" : 2,
    "AVL_CRC16": 4
    
}

print("TELTONIKA CODEC 8 EX FMC")
DATA_RAW = input('Input raw data: \n')

# Support function

def toAscii(input):
    output = binascii.unhexlify(input).decode("ASCII")
    return output

def unixTs(input):
    input = int(input, 16)
    return datetime.datetime.fromtimestamp(input / 1000).strftime('%Y-%m-%d %H:%M:%S')

def tsPriority(input):
    input = int(input, 16)
    switcher = {
        0: "Low",
        1: "High",
        2: "Panic",
    }
    return switcher.get(input, "invalid data")

def toBinary(input):
    input = int(input, 16)
    output = bin(input)[2:].zfill(32)
    return output


def longGps(input):
    pm = ""
    binary = toBinary(input)
    if(binary[0:1] == '0'):
        pm = True
    else:
        pm = False
        
    xor_result = int(binary, 2) ^ 0xFF
    hex_result = hex(xor_result)[2:].zfill(2)
    result = int(hex_result, 16) / 10000000
    
    if(pm == True):
        return result
    else:
        return result - result*2
    
def latGps(input):
    pm = ""
    binary = toBinary(input)
    if(binary[0:1] == '0'):
        pm = True
    else:
        pm = False
        
    xor_result = int(binary, 2) ^ 0xFFFFFFFF
    hex_result = hex(xor_result)[2:].zfill(2)
    result = int(hex_result, 16) / 10000000
    
    if(pm == True):
        return result
    else:
        return result - result*2
    
def valueCheck(input):
    input = int(input, 16)
    if (input != 0):
        return True
    return False
    

#Validation format

def CHECK_FORMAT(preamble, codec):
    if(str(preamble) == "00000000" and str(codec) == "8E"):
        return True
    else:
        return False
    
    
# ADAS parameter


#Main

def main(DATA):
    DATA = DATA.upper()
    data = {}

# imei length

    currentPos = 0
    lastPos = DATA_BYTE['IMEI_LEN']*2
    imei_length = DATA[currentPos:lastPos]
    
# imei
    
    currentPos = lastPos
    lastPos = lastPos+DATA_BYTE['IMEI']*2
    imei = DATA[currentPos:lastPos]
    
    data["imeiLen"] = int(imei_length, 16)
    data["imei"] = toAscii(imei)

# data

    dataPacket = []

    while(True):
# preamble

        currentPos = lastPos
        lastPos = lastPos+DATA_BYTE['AVL_PREAMBLE_LEN']*2
        preamble = DATA[currentPos:lastPos]

# data field length

        currentPos = lastPos
        lastPos = lastPos+DATA_BYTE["AVL_LENGTH_LEN"]*2
        dataLen = DATA[currentPos:lastPos]
    
# codec id length
    
        currentPos = lastPos
        lastPos = lastPos+DATA_BYTE["AVL_CODEC_ID_LEN"]*2
        codec = DATA[currentPos:lastPos]
    
# check validation of teltonika 8E codec
    
        if (CHECK_FORMAT(preamble, codec) == False):
            return "Invalid data format"

# num of data 1
        
        currentPos = lastPos
        lastPos = lastPos+DATA_BYTE["AVL_NUM_OF_DATA_1_LEN"]*2
        numOfDt1 = DATA[currentPos:lastPos]

# data packet
        
# AVL Data

        record = []
        for i in range(int(numOfDt1, 16)):
            
    # timestamp
            
            currentPos = lastPos
            lastPos = lastPos+DATA_BYTE["AVL_TIMESTAMP_LEN"]*2
            timeStamp = DATA[currentPos:lastPos]
            
    # timestamp priority
            
            currentPos = lastPos
            lastPos = lastPos+DATA_BYTE["AVL_PRIORITY_LEN"]*2
            priority = DATA[currentPos:lastPos]
            
    # gps element

    # longitude

            currentPos = lastPos
            lastPos = lastPos+DATA_BYTE["AVL_LONGITUDE_LEN"]*2
            longitude = DATA[currentPos:lastPos]
            
    # latitude
            currentPos = lastPos
            lastPos += DATA_BYTE["AVL_LATITUDE_LEN"]*2
            latitude = DATA[currentPos:lastPos]
            
    # altitude
            currentPos = lastPos
            lastPos += DATA_BYTE["AVL_ALTITUDE_LEN"]*2
            altitude = DATA[currentPos:lastPos]
            
    # angle
            currentPos = lastPos
            lastPos += DATA_BYTE["AVL_ANGLE_LEN"]*2
            angle = DATA[currentPos:lastPos]
            
    # satellite
            currentPos = lastPos
            lastPos += DATA_BYTE["AVL_SATELLITES_LEN"]*2
            satellite = DATA[currentPos:lastPos]
            
    # speed
            currentPos = lastPos
            lastPos += DATA_BYTE["AVL_SPEED_LEN"]*2
            speed = DATA[currentPos:lastPos]
            
            gpsElement = {}
            gpsElement["longitude"] = longGps(longitude)
            gpsElement["latitude"] = latGps(latitude)
            gpsElement["altitude"] = int(altitude, 16)
            gpsElement["angle"] = int(angle, 16)
            gpsElement["satellite"] = int(satellite, 16)
            gpsElement["speed"] = int(speed, 16)

                
    # end gps element
                
    # event io id
            currentPos = lastPos
            lastPos += DATA_BYTE["AVL_EVENT_IO_ID_LEN"]*2
            eventIoId = DATA[currentPos:lastPos]
            
    # n total id
            currentPos = lastPos
            lastPos += DATA_BYTE["AVL_N_TOTAL_IO_LEN"]*2
            nTotalId = DATA[currentPos:lastPos]
            
    # n1
            n1 = {}
    # n1 total io
            currentPos = lastPos
            lastPos += DATA_BYTE["AVL_N1_TOTAL_IO_LEN"]*2
            n1TotalIo = DATA[currentPos:lastPos]
            
    # n1 data
            n1Data = []
            if(valueCheck(n1TotalIo) == True):
                for i in range(int(n1TotalIo, 16)):

            # n1 io id
                    currentPos = lastPos
                    lastPos += DATA_BYTE["AVL_N1_IO_ID_LEN"]*2
                    n1IoId = DATA[currentPos:lastPos]
                    
            # n1 io value
                    currentPos = lastPos
                    lastPos += DATA_BYTE["AVL_N1_IO_VALUE_LEN"]*2
                    n1IoValue = DATA[currentPos:lastPos]
                    
                    n1Data.append({
                        "id": int(n1IoId, 16),
                        "value": int(n1IoValue, 16)
                    })
                    
            n1["n1TotalIo"] = int(n1TotalIo, 16)
            n1["n1Data"] = n1Data
            
    # n2
            n2 = {}
    # n2 total io
            currentPos = lastPos
            lastPos += DATA_BYTE["AVL_N2_TOTAL_IO_LEN"]*2
            n2TotalIo = DATA[currentPos:lastPos]
            
    # n2 data

            n2Data = []
            if(valueCheck(n2TotalIo) == True):
                for i in range(int(n2TotalIo, 16)):
                    
            # n2 io id
                    currentPos = lastPos
                    lastPos += DATA_BYTE["AVL_N2_IO_ID_LEN"]*2
                    n2IoId = DATA[currentPos:lastPos]
                    
            # n2 io value
                    currentPos = lastPos
                    lastPos += DATA_BYTE["AVL_N2_IO_VALUE_LEN"]*2
                    n2IoValue = DATA[currentPos:lastPos]
                    
                    n2Data.append({
                        "id": int(n2IoId ,16),
                        "value": int(n2IoValue, 16)
                    })
                    
            n2["n2TotalIo"] = int(n2TotalIo, 16)
            n2["n2Data"] = n2Data
                
    # n4
            n4 = {}
    # n4 total io
            currentPos = lastPos
            lastPos += DATA_BYTE["AVL_N4_TOTAL_IO_LEN"]*2
            n4TotalIo = DATA[currentPos:lastPos]
            
    # n4 data

            n4Data = []
            if(valueCheck(n4TotalIo) == True):
                for i in range(int(n4TotalIo, 16)):

            # n4 io id
                    currentPos = lastPos
                    lastPos += DATA_BYTE["AVL_N4_IO_ID_LEN"]*2
                    n4IoId = DATA[currentPos:lastPos]
                    
            # n4 io value
                    currentPos = lastPos
                    lastPos += DATA_BYTE["AVL_N4_IO_VALUE_LEN"]*2
                    n4IoValue = DATA[currentPos:lastPos]
                    
                    n4Data.append({
                        "id": int(n4IoId, 16),
                        "value": int(n4IoValue, 16)
                    })
                    
            n4["n4TotalIo"] = int(n4TotalIo, 16)
            n4["n4Data"] = n4Data
    # n8
            n8 = {}
            
    # n8 total io
            currentPos = lastPos
            lastPos += DATA_BYTE["AVL_N8_TOTAL_IO_LEN"]*2
            n8TotalIo = DATA[currentPos:lastPos]
            
    # n8 data

            n8Data = []
            if(valueCheck(n8TotalIo) == True):
                for i in range(int(n8TotalIo, 16)):

            # n8 io id
                    currentPos = lastPos
                    lastPos += DATA_BYTE["AVL_N8_IO_ID_LEN"]*2
                    n8IoId = DATA[currentPos:lastPos]
                    
            # n8 io value
                    currentPos = lastPos
                    lastPos += DATA_BYTE["AVL_N8_IO_VALUE_LEN"]*2
                    n8IoValue = DATA[currentPos:lastPos]
                
                    n8Data.append({
                        "id": int(n8IoId, 16),
                        "value": int(n8IoValue, 16)
                    })
                    
            n8["n8TotalIo"] = int(n8TotalIo, 16)
            n8["n8Data"] = n8Data
    # nx
            nx = {}
                
    # nx total io
            currentPos = lastPos
            lastPos += DATA_BYTE["AVL_NX_TOTAL_IO_LEN"]*2
            nxTotalIo = DATA[currentPos:lastPos]
            
    # nx data

            nxData = []
            if(valueCheck(nxTotalIo) == True):
                for i in range(int(nxTotalIo)):

            # nx io id
                    currentPos = lastPos
                    lastPos += DATA_BYTE["AVL_NX_IO_ID_LEN"]*2
                    nxIoId = DATA[currentPos:lastPos]
                    
            # nx io length
                    currentPos = lastPos
                    lastPos += DATA_BYTE["AVL_NX_IO_LENGTH_LEN"]*2
                    nxIoLength = DATA[currentPos:lastPos]
                    
            # nx io value
                    currentPos = lastPos
                    lastPos += int(nxIoLength, 16)*2
                    nxIoValue = data[currentPos:lastPos]
                    
                    nxData.append({
                        "id": int(nxIoId, 16),
                        "nxIoLength": int(nxIoLength, 16),
                        "nxIoValue": int(nxIoValue, 16)
                    })
                    
            nx["nxTotalIo"] = int(nxTotalIo, 16)
            nx["nxData"] = nxData

# number of data 2

        currentPos = lastPos
        lastPos += DATA_BYTE["AVL_NUM_OF_DATA_2_LEN"]*2
        numOfDt2 = DATA[currentPos:lastPos]

# crc 16
        currentPos = lastPos
        lastPos += DATA_BYTE["AVL_CRC16"]*2
        crc16 = DATA[currentPos:lastPos]

            
        record.append({
            "timeStamp": unixTs(timeStamp),
            "priority": tsPriority(priority),
            "gpsElement": gpsElement,
            "eventIoId": int(eventIoId, 16),
            "nTotalId": int(nTotalId, 16),
            "n1": n1,
            "n2": n2,
            "n4": n4,
            "n8": n8,
            "nx": nx
        })
        
        dataPacket.append({
            "preamble": preamble,
            "dataFieldLen": int(dataLen, 16),
            "codec": codec,
            "numOfData1": int(numOfDt1, 16),
            "record": record,
            "crc16": int(crc16, 16)
        })
        
        data["dataPacket"] = dataPacket
        
# Check if there is more data after crc

        if (DATA[lastPos:] ==  ""):
            return data


output = main(DATA_RAW)
print(json.dumps(output, indent=4))
