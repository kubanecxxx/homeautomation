<?php

class termostat_model extends CI_Model
{

    function getTopit()
    {
        $q = $this->db->query("select sp_topit()");
        $data = $q->result();
        $data = $data[0];
        $data = $data->{'sp_topit()'};
        return $data;
    }

    function getReqTemp()
    {
        $q = $this->db->query("select sp_requestedTemperature()");
        $data = $q->result();
        $data = $data[0];
        $data = $data->{'sp_requestedTemperature()'};
        return $data;
    }

    function getProgram()
    {
        $q = $this->db->query("select program.id,name from program inner join programy_names on program.id = programy_names.id where id_count = 100");
        $data = $q->result();
        $data = $data[0];
        return $data;
    }

    function getTemperatures()
    {
        $q = $this->db->query("select temperatures.sensor,value  value from temperatures inner join (select temperatures.sensor, max(cas) as ts from temperatures group by temperatures.sensor) maxt on (maxt.sensor=temperatures.sensor and maxt.ts = temperatures.cas  ) order by sensor ");      
        return $q;
    }
    
    function vata()
    {
        $a = $this->db->query("select * from temperatures limit 1");
        return $a;
    }

    function setProgram($prog_id)
    {
        $sql = sprintf("call sp_selectProgram(%d)", $prog_id);
        $this->db->query($sql);
    }

    function getPrograms()
    {
        $programy = $this->db->query('call sp_getProgramyNames()');
        
        foreach ($programy->result() as $row) {
            $data[$row->id] = array($row->name,$row->teplota);
        }
        
        return $data;
    }
    
    function setManualTemperature($temp)
    {
        $sql = sprintf('update programy set teplota = %d where id = 1',$temp);
        $this->db->query($sql);
    }
}
