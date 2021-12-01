#!/bin/bash

flash_led()
{	
	cnt=0
	while [ 1 ]
	do
		write_led 1
		sleep 0.1
		write_led 0
		sleep 0.1	
		echo "flash $cnt"
		cnt=$((cnt+1))
	done
}

set_power_output 1

speaker_beep()
{
	echo "speaker>"

	echo "run pigpiod"
	sudo pigpiod

	get_time_ms
	pigpiod_wait_tm0=$msec
	
#最多等10s
	while [ 1 ]
	do
#		pigs hp 19 1000 500000
		pigs hp 19 1000 $pigs_pwm
		speaker_ret=$?
		echo "speaker_ret: $speaker_ret"
		if [ $speaker_ret -eq 0 ];then
			echo "wait pigpiod server ok"
			break
		fi
		
		get_time_ms
		delta=$((msec-pigpiod_wait_tm0))
		echo "wait ms: $delta"
		if [ $delta -ge 10000 ];then
			echo "wait pigpiod time out"
			return
		fi

		sleep 0.1
	done

	sleep 1
	pigs hp 19 1000 0

	echo "speaker<"
}

speaker_beep

