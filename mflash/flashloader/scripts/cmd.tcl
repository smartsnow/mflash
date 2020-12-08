######################################
# Author : Snow Yang
# Date   : 2018-12-03
# Mail   : yangsw@mxchip.com
######################################

set CMD_READ  0
set CMD_WRITE 1
set CMD_ERASE 2
set CMD_MAC   3
set CMD_UNLOCK 4

proc mflash_erase { addr size } {

    mww $::MFLASH_CMD_LOC $::CMD_ERASE
    mww $::MFLASH_ARG0_LOC $addr
    mww $::MFLASH_ARG1_LOC $size

    mflash_cmd_run 10000
}

proc mflash_write { file addr } {

    set percent 0
    set size [file size $file]
    set remain $size
    while {$remain > 0} {
        set n $($remain > $::mflash_buf_size ? $::mflash_buf_size : $remain)
        mww $::MFLASH_CMD_LOC $::CMD_WRITE
        mww $::MFLASH_ARG0_LOC $addr
        mww $::MFLASH_ARG1_LOC $n
        load_image_bin $file $($size - $remain) $::MFLASH_BUF_LOC $n
        set remain $($remain - $n)
        set addr $($addr + $n)

        mflash_cmd_run 1000
        
        set percent_now $(($size - $remain) * 100 / $size)
        if { $percent_now > $percent } {
            set percent $percent_now
            puts "$percent%"
        }
    }
}

proc mflash_read { file addr size } {

    file delete -force $file

    set percent 0
    set remain $size
    while {$remain > 0} {
        set n $($remain > $::mflash_buf_size ? $::mflash_buf_size : $remain)
        mww $::MFLASH_CMD_LOC $::CMD_READ
        mww $::MFLASH_ARG0_LOC $addr
        mww $::MFLASH_ARG1_LOC $n
        set remain $($remain - $n)
        set addr $($addr + $n)

        mflash_cmd_run 1000

        dump_image $file $::MFLASH_BUF_LOC $n 1

        set percent_now $(($size - $remain) * 100 / $size)
        if { $percent_now > $percent } {
            set percent $percent_now
            puts "$percent%"
        }
    }
}

proc mflash_mac { } {
    
    mww $::MFLASH_CMD_LOC $::CMD_MAC

    mflash_cmd_run 1000

    mem2array mac_arr 8 $::MFLASH_BUF_LOC 6
    set mac_val [expr $mac_arr(5)+($mac_arr(4)<<8)+($mac_arr(3)<<16)+($mac_arr(2)<<24)+($mac_arr(1)<<32)+($mac_arr(0)<<40)]

    puts [format "%012X" $mac_val]
}

proc mflash_unlock { } {
    
    mww $::MFLASH_CMD_LOC $::CMD_UNLOCK

    mflash_cmd_run 1000
}