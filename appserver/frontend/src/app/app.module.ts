import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { HttpClientModule } from '@angular/common/http';
import { MatButtonToggleModule } from '@angular/material';

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
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
		NgbModule.forRoot(),
    MatButtonToggleModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
