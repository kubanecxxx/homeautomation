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
//        $q = $this->db->query("select temperatures.sensor,value value, cas from temperatures inner join (select temperatures.sensor, max(cas) as ts from temperatures group by temperatures.sensor) maxt on (maxt.sensor=temperatures.sensor and maxt.ts = temperatures.cas  ) order by sensor ");
        /*
        $q = $this->db->query("select events.sensor,value value, cas from temperatures \
            inner join (select temperatures.sensor, max(cas) as ts from temperatures group by \
            temperatures.sensor) maxt on (maxt.sensor=temperatures.sensor and maxt.ts = temperatures.cas  ) \
            order by sensor ");
            
           */
        $query = "select event from events where event_id = 304 order by cas desc limit 1";
        $water = $this->db->query($query)->result();
        $query = "select event from events where event_id = 305 order by cas desc limit 1";
        $home = $this->db->query($query)->result();
        
        $water =  $water[0]->event;
        $home = $home[0]->event;
        
        $q = (object) array ("home" => $home, "water" => $water) ;
        //$q = $this->db->query("call sp_lastTemperatures()");
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
            $data[$row->id] = array(
                $row->name,
                $row->teplota
            );
        }
        
        return $data;
    }

    function setManualTemperature($temp)
    {
        $sql = sprintf('update programy set teplota = %d where id = 1', $temp);
        $this->db->query($sql);
    }

    function heatingIsAlive()
    {
        $query = "select event,cas from events where event_id = 300 and pipe = 201 order by cas desc limit 1";
        $a = $this->db->query($query);
        $b = $a->result();
        $b = $b[0];
        
        return $b;
    }

    function getVodaScreen()
    {
        // t1,t2 start stop
        // teplota
        // hlidat teplotu
        $query = "select teplota,start,stop,number from programy where id = 2";
        $a = $this->db->query($query);
        $b = $a->result();
        return $b;
    }

    function setVodaData($data)
    {
        for ($i = 0; $i < 2; $i ++) {
            // print_r($data[$i]);
            $d = $data[$i];
            $query = sprintf("call sp_configureProgram(2,%f,\"%s\",\"%s\",NULL,%d)", $d->teplota, $d->start, $d->stop, $i);
            // echo $query;
            $this->db->query($query);
        }
    }

    function getHeatingData($weekend)
    {
        // hlidat teplotu
        $query = sprintf("select teplota,start,stop,number from programy where id = 3 and weekend = %d order by number asc", $weekend);
        $a = $this->db->query($query);
        $b = $a->result();
        return $b;
    }

    function setHeatingData($data)
    {
        for ($i = 0; $i < count($data); $i ++) {
            $d = $data[$i];
            $query = sprintf("call sp_configureProgram(3,%f,\"%s\",NULL,%d,%d)", $d->temperature, $d->start, $d->weekend, $i % 4);
            
            $this->db->query($query);
        }
    }
}
