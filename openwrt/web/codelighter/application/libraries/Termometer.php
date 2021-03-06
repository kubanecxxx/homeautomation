<?php

if (! defined('BASEPATH'))
    exit('No direct script access allowed');

class Termometer
{

    var $offset;

    public function Termometer()
    {
        $this->offset = 0;
    }

//     public function getImg($temperature, $water = 0, $attr = NULL)
//     {
//         $this->offset = 0;
//         $height = 220;
//         $width = 110;
        
//         $minimumTemperature = 13;
//         $maximumTemperature = 25;
        
//         $waves = "none";
//         if ($water) {
//             $this->offset = 20;
            
//             $width += 20;
//             $waves = "inline";
//         }
        
//         $CI = &get_instance();
//         $CI->load->helper('file');
//         $start = read_file(getcwd() . '/css/obr.svg');
        
//         // compute this number
//         $origin = - 10;
        
//         $neco = - (($temperature - 12.5) * 10);
        
//         $data = sprintf($start, $attr, $width, $height, $this->offset, $waves, $this->offset, min(max($neco, - 140), 0));
        
//         for ($i = 0; $i < 27; $i ++)
//             $data = $data . $this->getLine($i);
//         $data = $data . $this->getLabel($temperature, 150 + $neco);
//         $data = $data . '  </svg>';
//         return $data;
//     }

    public function getImg($temperature, $water = 0, $minimumTemperature = 12.5, $divide = 1, $attr = NULL)
    {
        $this->offset = 0;
        $height = 220;
        $width = 110;
        
        $waves = "none";
        if ($water) {
            $this->offset = 20;
            
            $width += 20;
            $waves = "inline";
        }
        
        $CI = &get_instance();
        $CI->load->helper('file');
        $start = read_file(getcwd() . '/css/obr.svg');
        
        $neco = - (($temperature - $minimumTemperature) * (10 / $divide));
        $len = min(max($neco, - 140), 0);
        
        $data = sprintf($start, $attr, $width, $height, $this->offset, $waves, $this->offset, $len);
        
        $ch = 0;
        if ($divide != 1)
            $ch = 1;
        
        for ($i = 0; $i < 27; $i ++)
            $data = $data . $this->getLine($i, $ch);
        
        $data = $data . $this->getLabel($temperature, 150 + $neco);
        $data = $data . '  </svg>';
        return $data;
    }

    private function getLabel($temp, $pos)
    {
        $pos = min(max($pos, 20), 140);
        $fmt = '<text x="%d" y="%d" fill=white>%.1f&deg;C</text>';
        $data = sprintf($fmt, $this->offset + 45, $pos, $temp);
        return $data;
    }

    private function getLine($idx, $allLong = 0)
    {
        $ja = 26 + $this->offset;
        if ($idx % 2 == 0 && !$allLong)
            $ja += 3;

        if ($allLong)
            $ja += 3;
        
        $zero = 140 - $idx * 5;
        $fmt = '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="green" stroke-width="2" />';
        $data = sprintf($fmt, $this->offset + 18, $zero, $ja, $zero);
        return $data;
    }
}
?>