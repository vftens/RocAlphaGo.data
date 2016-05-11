#!/usr/bin/env python
import sys
import json
import matplotlib.pyplot as plt

if len(sys.argv) > 1:
	with open(sys.argv[1], 'r') as f:
		metadata = json.load(f)
		n_epochs = len(metadata['epochs'])

		if len(sys.argv) > 2:
			prefix = sys.argv[2]
		else:
			prefix = ''

		# LOSS PLOT

		train_loss = [ep['loss'] for ep in metadata['epochs']]
		val_loss = [ep['val_loss'] for ep in metadata['epochs']]

		plt.figure()
		plt.plot(range(n_epochs), train_loss)
		plt.plot(range(n_epochs), val_loss)
		plt.xlabel('epoch')
		plt.legend(['train_loss', 'val_loss'], loc='upper right')
		plt.savefig(prefix + 'loss.png')

		# ACCURACY PLOT

		train_acc = [ep['acc'] for ep in metadata['epochs']]
		val_acc = [ep['val_acc'] for ep in metadata['epochs']]

		plt.figure()
		plt.plot(range(n_epochs), train_acc)
		plt.plot(range(n_epochs), val_acc)
		plt.xlabel('epoch')
		plt.legend(['train_acc', 'val_acc'], loc='lower right')
		plt.savefig(prefix + 'acc.png')
else:
	print "usage: python plot_epochs.py METADATA_FILE"
