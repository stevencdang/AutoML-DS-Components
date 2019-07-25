ALTER TABLE `workflow_component_instance` CHANGE COLUMN `state` `state` ENUM('new','running','running_dirty','error','do_not_run','completed', 'completed_warn') NULL DEFAULT 'new' COLLATE 'utf8_bin' AFTER `dirty_selection`;
ALTER TABLE `workflow_component_instance_persistence` CHANGE COLUMN `state` `state` ENUM('new','running','running_dirty','error','do_not_run','completed', 'completed_warn') NULL DEFAULT 'new' COLLATE 'utf8_bin' AFTER `dirty_selection`;
ALTER TABLE `workflow_component_instance` ADD COLUMN `warnings` LONGTEXT NULL COLLATE 'utf8_bin' AFTER `errors`;
ALTER TABLE `workflow_component_instance_persistence` ADD COLUMN `warnings` LONGTEXT NULL COLLATE 'utf8_bin' AFTER `errors`;
