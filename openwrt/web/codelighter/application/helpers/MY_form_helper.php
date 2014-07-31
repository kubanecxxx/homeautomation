<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

if ( ! function_exists('form_dropdown_kuba'))
{
    function form_dropdown_kuba($name = '', $options = array(), $selected = array(), $extra = '')
    {
        if ( ! is_array($selected))
        {
            $selected = array($selected);
        }

        // If no selected state was submitted we will attempt to set it automatically
        if (count($selected) === 0)
        {
            // If the form name appears in the $_POST array we have a winner!
            if (isset($_POST[$name]))
            {
                $selected = array($_POST[$name]);
            }
        }

        if ($extra != '') $extra = ' '.$extra;

        $multiple = (count($selected) > 1 && strpos($extra, 'multiple') === FALSE) ? ' multiple="multiple"' : '';

        $form = '<select name="'.$name.'"'.$extra.$multiple.">\n";

        foreach ($options as $key => $val)
        {
            $key = (string) $key;

            if (is_array($val) && ! empty($val))
            {
                $sel = (in_array($key, $selected)) ? ' selected="selected"' : '';
                
                $form .= '<option value="'.$key.'"'.$sel.' temperature = "' .$val[1]. '">'.(string) $val[0]."</option>\n";
            }
            else
            {
                $sel = (in_array($key, $selected)) ? ' selected="selected"' : '';

                $form .= '<option value="'.$key.'"'.$sel.'>'.(string) $val."</option>\n";
            }
        }

        $form .= '</select>';

        return $form;
    }
}

?>