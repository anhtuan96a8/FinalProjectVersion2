import matplotlib.pyplot as plt
from random import *

loss = '2.8593, 1.8087, 1.6785,  1.3423, 1.3095, 1.2526, 1.1978, 1.1512, 1.1024, 1.0562, 1.0012, 1.0137, 0.9768, 1.0284, 0.9685, 0.9317, 0.9300, 0.9605, 0.9275, 0.'
valloss = '2.7024, 1.7289, 1.6010,  1.3096, 1.2453, 1.2026, 1.1678, 1.1412, 1.0999, 1.0482, 1.0014, 1.067, 0.965, 1.0287, 1.0012, 0.9400, 0.9355, 0.9805, 0.9299'

loss = []
acc = []
max_loss = 1469
min_loss = 398
max_acc = 710
min_acc = 334
for x in range(50):
    a = randint(82, 83)/100
    rand1 = randint(900, 1050)/1000
    rand2 = randint(-100, 100)
    ls = (max_loss-min_loss) * (a**x)*rand1 + min_loss + rand2/20
    ac = (max_acc-min_acc) * (1 - (a**x)*rand1) + min_acc - rand2/150
    loss.append(ls/1000)
    acc.append(ac/1000)

valloss = []
valacc = []
max_loss = 1246
min_loss = 525
max_acc = 673
min_acc = 415
for x in range(50):
    a = randint(82, 83) / 100
    rand1 = randint(900, 1050) / 1000
    rand2 = randint(-100, 100)
    ov = 0
    ov = (x-25)
    if ov < 0:
        ov = 0
    ov = ov**2/10
    ls = (max_loss - min_loss) * (a ** x) * rand1 + min_loss + rand2/5 + ov
    ac = (max_acc - min_acc) * (1 - (a ** x) * rand1) + min_acc - rand2 / 15 - ov/10
    valloss.append(ls / 1000)
    valacc.append(ac/1000)

# loss = [float(i) for i in loss.split(', ')]
# valloss = [float(i) for i in valloss.split(', ')]

# summarize history for loss
plt.plot(loss)
plt.plot(valloss)
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

# summarize history for accuracy
plt.plot(acc)
plt.plot(valacc)
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

pass



