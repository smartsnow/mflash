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

proc erase { addr size } {

    mww $::FLASH_ALG_CMD_LOC $::CMD_ERASE
    mww $::FLASH_ALG_ARG0_LOC $addr
    mww $::FLASH_ALG_ARG1_LOC $size

    flash_alg_cmd_run 10000
}

proc write { file addr } {

    set size [file size $file]
    set remain $size
    while {$remain > 0} {
        set n $($remain > $::FLASH_ALG_BUF_SIZE ? $::FLASH_ALG_BUF_SIZE : $remain)
        mww $::FLASH_ALG_CMD_LOC $::CMD_WRITE
        mww $::FLASH_ALG_ARG0_LOC $addr
        mww $::FLASH_ALG_ARG1_LOC $n
        load_image_bin $file $($size - $remain) $::FLASH_ALG_BUF_LOC $n
        set remain $($remain - $n)
        set addr $($addr + $n)

        flash_alg_cmd_run 1000
        puts stderr "-->0x[format %x $($size - $remain)]"
    }
}

proc read { file addr size } {
    exec echo -n > $file

    set remain $size
    set tmpfile "tmp.bin"
    while {$remain > 0} {
        set n $($remain > $::FLASH_ALG_BUF_SIZE ? $::FLASH_ALG_BUF_SIZE : $remain)
        mww $::FLASH_ALG_CMD_LOC $::CMD_READ
        mww $::FLASH_ALG_ARG0_LOC $addr
        mww $::FLASH_ALG_ARG1_LOC $n
        set remain $($remain - $n)
        set addr $($addr + $n)

        flash_alg_cmd_run 1000

        dump_image $tmpfile $::FLASH_ALG_BUF_LOC $n
        exec cat $tmpfile >> $file
        exec rm $tmpfile
    }
}

proc mac { } {
    
    mww $::FLASH_ALG_CMD_LOC $::CMD_MAC

    flash_alg_cmd_run 1000

    mem2array mac_arr 8 $::FLASH_ALG_BUF_LOC 6
    set mac_val [expr $mac_arr(5)+($mac_arr(4)<<8)+($mac_arr(3)<<16)+($mac_arr(2)<<24)+($mac_arr(1)<<32)+($mac_arr(0)<<40)]

    puts [format "%012X" $mac_val]
}

proc unlock { } {
    
    mww $::FLASH_ALG_CMD_LOC $::CMD_UNLOCK

    flash_alg_cmd_run 1000
}