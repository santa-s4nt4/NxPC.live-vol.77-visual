"""
CHOP Execute DAT

me - this DAT

Make sure the corresponding toggle is enabled in the CHOP Execute DAT.
"""

import random

def onOffToOn(channel: Channel, sampleIndex: int, val: float, 
			  prev: float):
	"""
	Called when a channel changes from 0 to non-zero.
	
	Args:
		channel: The Channel object which has changed
		sampleIndex: The index of the changed sample
		val: The numeric value of the changed sample
		prev: The previous sample value
	"""
	# info3 の値を取得（上限値）
	max_val = int(op('info3')[0])-1

	# 値を保存するConstant CHOPを取得
	out_chop = op('target_val')
	current_val = int(out_chop[0]) # 現在出力されている数値

	# 上限が0以下の場合は0を入れて終了（フリーズ防止のセーフティ）
	if max_val <= 1:
		out_chop.par.value0 = 1
		return

	new_val = current_val
	
	# 新しい数字が今の数字と同じである限り、ランダム生成を引き直す
	while new_val == current_val:
		new_val = random.randint(1, max_val)
		
	# Constant CHOPの値を更新
	out_chop.par.value0 = new_val
	op('speed1').par.resetpulse.pulse()

	return

def whileOn(channel: Channel, sampleIndex: int, val: float, 
			prev: float):
	"""
	Called every frame while a channel is non-zero.
	
	Args:
		channel: The Channel object which has changed
		sampleIndex: The index of the changed sample
		val: The numeric value of the changed sample
		prev: The previous sample value
	"""
	return

def onOnToOff(channel: Channel, sampleIndex: int, val: float, 
			  prev: float):
	"""
	Called when a channel changes from non-zero to 0.
	
	Args:
		channel: The Channel object which has changed
		sampleIndex: The index of the changed sample
		val: The numeric value of the changed sample
		prev: The previous sample value
	"""
	return

def whileOff(channel: Channel, sampleIndex: int, val: float, 
			 prev: float):
	"""
	Called every frame while a channel is 0.
	
	Args:
		channel: The Channel object which has changed
		sampleIndex: The index of the changed sample
		val: The numeric value of the changed sample
		prev: The previous sample value
	"""
	return

def onValueChange(channel: Channel, sampleIndex: int, val: float, 
				  prev: float):
	"""
	Called when a channel value changes.
	
	Args:
		channel: The Channel object which has changed
		sampleIndex: The index of the changed sample
		val: The numeric value of the changed sample
		prev: The previous sample value
	"""
	return
