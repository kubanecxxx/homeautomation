<?php

class termostat extends CI_Controller
{

    private function _page($data = NULL, $title = NULL)
    {
        if ($this->uri->segment(2))
            $page = $this->uri->segment(2) . '_content';
        else
            $page = 'index_content';
        
        if ($title)
            $data['title'] = $title;
        else
            $data['title'] = str_replace('_content', '', $page);
        
        $post = $this->input->post();
        if ($post['ajax']) {
            $this->load->view('pages/' . $page, $data);
        } else {
            $data['title'] = ucfirst($data['title']);
            $data['main_content'] = 'pages/' . $page;
            $this->load->view('include/template', $data);
        }
    }

    public function def()
    {}

    public function index($page = NULL)
    {
        if ($page == NULL) {
            
            $this->load->model('termostat_model');
            $this->load->helper('date');
            
            $data['zije'] = $this->termostat_model->heatingIsAlive();
            $data['program'] = $this->termostat_model->getProgram();
            $data['topit'] = $this->termostat_model->getTopit();
            $data['teploty'] = $this->termostat_model->getTemperatures();
            $data['programy'] = $this->termostat_model->getPrograms();
            
            // rint_r($data['teploty']);
            
            $this->load->library("termometer");
            $this->_page($data);
        }
    }

    public function submit_program()
    {
        $this->load->model('termostat_model');
        
        $par = $this->input->post();
        $this->termostat_model->setProgram($par["programy"]);
        
        if ($par['programy'] == 1) {
            $this->termostat_model->setManualTemperature($par['teplota']);
        }
        
        if ($this->input->post('ajax')) {
            
            $this->load->library("termometer");
            
            $data['topit'] = $this->termostat_model->getTopit();
            $data['program'] = $this->termostat_model->getProgram();
            $data['teploty'] = $this->termostat_model->getTemperatures();
            $data['programy'] = $this->termostat_model->getPrograms();
            
            $arr = $data['teploty']->result();
            
            $this->load->view("pages/index_content", $data);
        } else {
            redirect("/");
        }
    }

    public function teplomer()
    
    {
        $this->load->library("termometer");
        $this->_page();
    }

    public function voda($cislo = NULL)
    {
        if ($cislo)
            echo $cislo;
        $this->load->library("termometer");
        $this->_page();
    }
}