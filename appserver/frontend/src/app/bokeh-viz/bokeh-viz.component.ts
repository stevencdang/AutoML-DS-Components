import { Component, OnInit, ViewChild, ElementRef, Renderer } from '@angular/core';
import { DataService } from "../lib/data.service";

declare let swal: any;

@Component({
  selector: 'app-bokeh-viz',
  templateUrl: './bokeh-viz.component.html',
  styleUrls: ['./bokeh-viz.component.scss']
})
export class BokehVizComponent implements OnInit {

  htmlSnippet: string = '<script>alert("Initialized bokeh app by bypassing angular security")</script>';
  //htmlSnippet: string = "Test html snippet";
  @ViewChild('element') public viewElement: ElementRef;
  public element: any;

  constructor(public renderer: Renderer,
              private dataService: DataService
              ) {}
  
  public ngOnInit()
  {
     //this.appendHTMLSnippetToDOM();
     //this.dataService.testBokeh().subscribe(result => this.htmlSnippet = result['script']);
     //this.dataService.testBokeh().subscribe(result => console.log(result['script']));
     //this.dataService.testBokeh().subscribe(result => console.log("testBokeh"));
  }

  public test1()
  {
    console.log("Testing1");
     this.dataService.testBokeh1().subscribe(result => console.log(result['script']));
     //this.dataService.testBokeh().subscribe(result => this.appendHTMLSnippetToDOM(result['script']));
    //this.element = this.viewElement.nativeElement;
    //const fragment = document.createRange().createContextualFragment(this.htmlSnippet);
    //this.element.appendChild(fragment);
  }
  
  public test2()
  {
    console.log("Testing2");
     this.dataService.testBokeh2().subscribe(result => console.log(result['script']));
    //this.dataService.testBokeh().subscribe(result => this.appendHTMLSnippetToDOM(result['script']));
    //
  }
  public appendHTMLSnippetToDOM(htmlSnippet: string)
  {
    console.log("appending snippet");
    this.htmlSnippet = htmlSnippet;
    this.element = this.viewElement.nativeElement;
    const fragment = document.createRange().createContextualFragment(this.htmlSnippet);
    this.element.appendChild(fragment);
  }

}
