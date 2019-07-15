import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { HttpClientModule } from '@angular/common/http';
import { MatButtonToggleModule } from '@angular/material';
import { MatListModule } from '@angular/material/list';
import { MatButtonModule } from '@angular/material/button'; 

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TabbedInterfaceComponent } from './tabbed-interface/tabbed-interface.component';
import { VariableExplorerComponent } from './variable-explorer/variable-explorer.component';
import { SimpleDatasetEdaComponent } from './simple-dataset-eda/simple-dataset-eda.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { SanitizePipe } from './lib/sanitize.pipe';
import { BokehVizComponent } from './bokeh-viz/bokeh-viz.component';
import { DatasetImporterComponent } from './dataset-importer/dataset-importer.component';
import { NotReadyYetComponent } from './not-ready-yet/not-ready-yet.component';
import { ProblemCreatorComponent } from './problem-creator/problem-creator.component';

@NgModule({
  declarations: [
    AppComponent,
    TabbedInterfaceComponent,
    VariableExplorerComponent,
    SimpleDatasetEdaComponent,
    PageNotFoundComponent,
    SanitizePipe,
    BokehVizComponent,
    DatasetImporterComponent,
    NotReadyYetComponent,
    ProblemCreatorComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
		NgbModule.forRoot(),
    MatButtonToggleModule,
    MatListModule,
    MatButtonModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
