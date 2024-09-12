### Magnetization transfer in 4D HCNH NOESY (HSQC-NOESY-HMQC)

1. All protons are excited
2. A filter is applied that preserves only magnetization transferred from the amide protons through bond to the amide nitrogens
3. Magnetization is transferred through space to all protons
4. A filter is applied that preserves only magnetization transferred from the aliphatic protons through bond to the covalently bonded carbon
5. Magnetization is transferred back through bond from the aliphatic carbon to the covalently bonded protons
6. From the aliphatic protons the magnetization is transferred to the detector.
HSQC (1-2) and HMQC (4-5) pulses allow magnetization through bonds only, while the NOESY pulse (3) allows magnetization through space only.

        ;noehcnhwg4d_nove

        ;avance version
        ;4D 13C,15N-edited NOESY (HMQC-NOESY-HSQC)
        ;F1 1H (semi-constant time)
        ;F2 13C
        ;F3 15N
        ;F4 1HN
        ;water suppression with water gate

        ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
        ; Written by Jiri Novacek & Konstantinos Tripsianes, CEITEC Masaryk University
        ;
        ; Please cite: Evangelidis T. et al. (2018) Nat. Communications 9(384).
        ; DOI: 10.1038/s41467-017-02592-z 
        ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

        prosol relations=<triple>

        #include<Avance.incl>
        #include<Grad.incl>
        #include<Delay.incl>

        "p2=p1*2"
        "p22=p21*2"
        "d11=20m"
        "d12=20u"
        "d13=4u"

        "d4=1.5m"
        "d3=d4-p16-d16"
        "d26=1/(cnst4*4)"
        "d18=50u"
        "p18=d26-d18-4u"

        "d29=d9-p21-p17-1m"

        "d31=d4-p15-d16"
        "d51=3u"
        "d41=d4+p8+d51-p15-d16"

        "in31=inf1/4"

        "FACTOR1=d41*10000000*2/td1"
        "in41=FACTOR1/10000000"

        "if ( in41 > in31 ) { in51 = 0; } else { in51=in31-in41; }"
        "if ( in41 > in31 ) { in41 = in31; }"

        "in32=inf2/2"
        "d32=in32-p22/2-p3*0.637"

        "d33=3u"
        "in33=inf3/2"

        "DELTA=d33+p14-p2/2+2u"
        "DELTA1=d26-p16-p11-12u"

        "spoff5=bf2*(cnst22/1000000)-o2"
        "spoff6=bf2*(cnst21/1000000)-o2"
        "spoff13=bf2*(cnst24/1000000)-o2"

        1 ze
          d11 pl16:f3
        2 d11 do:f3
          d11 
        3 d1  
          d12 
          d12 pl1:f1 pl2:f2 pl3:f3
          d12 fq=cnst23(bf ppm):f2
          50u UNBLKGRAD

          (p3 ph1):f2
          p17:gp1
          1m pl0:f2

          (p1 ph8):f1
          p15:gp7
          d16
          d31
          (p8:sp13 ph1):f2
          d51
          (p2 ph1):f1
          d41 pl2:f2
          p15:gp8
          d16
          (p3 ph6):f2
          d32
          (center (p2 ph1):f1 (p22 ph1):f3)
          d32
          (p3 ph1):f2
          p15:gp8
          d16
          d31 pl0:f2
          (p8:sp13 ph1):f2
          d51
          (p2 ph1):f1
          d41
          p15:gp7
          d16
          (p1 ph1):f1

          d29
          (p21 ph1):f3
          p17:gp2
          1m

          (p1 ph1)
          4u
          p18:gp3
          d18
          (center (p2 ph1) (p22 ph1):f3 )
          4u
          p18:gp3
          d18
          (p1 ph2) 

          p20:gp4
          d16

          (p21 ph3):f3
          d33
          (center (p2 ph1):f1 (p14:sp5 ph1 4u p14:sp6 ph1):f2 )
          d33
          (p22 ph1):f3
          DELTA
          (p2 ph1):f1
          DELTA
          (p21 ph4):f3
          4u
          p16:gp5
          d16 pl0:f1
          (p11:sp1 ph7):f1
          4u
          4u pl1:f1
          (p1 ph1) 
          4u
          p16:gp6
          DELTA1 pl0:f1
          (p11:sp1 ph7):f1
          4u
          4u pl1:f1
          (center (p2 ph1) (p22 ph1):f3 )
          4u pl0:f1
          (p11:sp1 ph7):f1
          4u
          p16:gp6
          DELTA1 pl16:f3
          4u BLKGRAD
          go=2 ph31 cpd3:f3
          d11 do:f3 mc #0 to 2 
            F1PH(calph(ph8, +90), caldel(d31, +in31) & caldel(d51, +in51) & caldel(d41, -in41))
            F2PH(calph(ph6, +90), caldel(d32, +in32))
            F3PH(calph(ph3, +90), caldel(d33, +in33))

        exit

        ph1=0
        ph2=1
        ph3=0 0 2 2
        ph4=0
        ph5=0
        ph6=0 2
        ph7=2
        ph8=0 0 0 0 2 2 2 2
        ph31=0 2 2 0 2 0 0 2

        ;pl0 : 0W
        ;pl1 : f1 channel - power level for pulse (default)
        ;pl2 : f2 channel - power level for pulse (default)
        ;pl3 : f3 channel - power level for pulse (default)
        ;pl16: f3 channel - power level for CPD/BB decoupling

        ;sp1: f1 channel - shape for p11 pulse [sinc1.1000]
        ;sp5: f2 channel - shape for p14 pulse [Q3.1000]
        ;sp6: f2 channel - shape for p14 pulse [Q3.1000]
        ;sp13: shape for adiabatic pulse p8 [Crp60,0.5,20.1]

        ;p1 : f1 channel -  90 degree high power pulse
        ;p3 : f2 channel -  90 degree high power pulse
        ;p8 : f2 channel -  adiabatic pulse [500u]
        ;p11: f1 channel -  90 degree shaped pulse [1.1 msec]
        ;p21: f3 channel -  90 degree high power pulse
        ;p14: f2 channel - 180 degree shaped pulse

        ;d4:  1/(4J(CH)    [1.5-1.7 msec]
        ;d9:  noesy mixing [70-120ms]

        ;cnst4 : J(NH)
        ;cnst21: CO chemical shift (offset, in ppm)
        ;cnst22: Calpha chemical shift (offset, in ppm)
        ;cnst23: Caliphatic chemical shift (offset, in ppm)
        ;o2p: Caliphatic chemical shift (cnst23)
        ;cnst24: Caliphatic, Caromatic chemical shift [70-75ppm]

        ;FnMODE: States in F1
        ;FnMODE: States in F2
        ;FnMODE: States in F3

        ;p15: 200u
        ;p16: 1000u
        ;p17: 500u
        ;p20: 1500u

        ;gpnam1: sine100
        ;gpnam2: sine100
        ;gpnam3: rect1
        ;gpnam4: sine100
        ;gpnam5: sine100
        ;gpnam6: sine100
        ;gpnam7: sine32
        ;gpnam8: sine32

        ;gpz1: 29%
        ;gpz2: 12%
        ;gpz3: 3%
        ;gpz4: 31%
        ;gpz5: 57%
        ;gpz6: 71%
        ;gpz7: 23%
        ;gpz8: 17%
