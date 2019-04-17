import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-tabbed-interface',
  templateUrl: './tabbed-interface.component.html',
  styleUrls: ['./tabbed-interface.component.scss']
})
export class TabbedInterfaceComponent implements OnInit {
  
  tabs: string[] = [
    "Variable-Viewer",
    "Raw-Data-Explorer"
  ];
 
  
	activeTab: string = "Raw-Data-Explorer";
	activeTabId: string;

	currentJustify = "fill";

  constructor() { 
		this.activeTabId = `tb-${this.activeTab}`;
	
	}


  ngOnInit() {
  }

}
