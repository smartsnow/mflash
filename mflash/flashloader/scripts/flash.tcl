######################################
# Author : Snow Yang
# Date   : 2018-12-03
# Mail   : yangsw@mxchip.com
######################################

set MFLASH_ENTRY_LOC     $($MFLASH_CONFIG_START + 0x00)
set MFLASH_BUF_SIZE_LOC  $($MFLASH_CONFIG_START + 0x04)
set MFLASH_RDY_LOC       $($MFLASH_CONFIG_START + 0x08)
set MFLASH_CMD_LOC       $($MFLASH_CONFIG_START + 0x0C)
set MFLASH_RET_LOC       $($MFLASH_CONFIG_START + 0x10)
set MFLASH_ARG0_LOC      $($MFLASH_CONFIG_START + 0x14)
set MFLASH_ARG1_LOC      $($MFLASH_CONFIG_START + 0x18)
set MFLASH_BUF_LOC       $($MFLASH_CONFIG_START + 0x1C)

proc memread32 {address} {
    
    mem2array memar 32 $address 1
    return $memar(0)
}

proc load_image_bin {fname foffset address length } {

    load_image $fname [expr $address - $foffset] bin $address $length
}

proc mflash_init { mloader } {

    global mflash_buf_size

    load_image $mloader

    set mflash_entry [memread32 $::MFLASH_ENTRY_LOC]
    set mflash_buf_size [memread32 $::MFLASH_BUF_SIZE_LOC]
	
    reg pc $mflash_entry

    if { $::MFLASH_RUN_WITH_HALT == 0 } {
        resume
    }
}

proc mflash_cmd_run { timeout } {

    mww $::MFLASH_RDY_LOC 1

    loop t 0 $timeout 1 {
        if { $::MFLASH_RUN_WITH_HALT == 1 } {
            resume
        }
        after 3
        if { $::MFLASH_RUN_WITH_HALT == 1 } {
            halt
        }
        set ret [memread32 $::MFLASH_RDY_LOC]  
        if { $ret == 0 } {
            set ret [memread32 $::MFLASH_RET_LOC]
            return $ret
        }
    }
    
    error "error"
    exit -1;
}
