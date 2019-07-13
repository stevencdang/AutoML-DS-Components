import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { SimpleDatasetEdaComponent } from './simple-dataset-eda/simple-dataset-eda.component';
import { DatasetImporterComponent } from './dataset-importer/dataset-importer.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

const routes: Routes = [
    { path: 'eda/:wfid',      
      component: SimpleDatasetEdaComponent 
    },
    { path: 'datasetimporter/:wfid',      
      component: DatasetImporterComponent
    },
    { path: '', component: PageNotFoundComponent },
    //{ path: '',
      //redirectTo: 'eda',
      //pathMatch: 'full'
    //},
    { path: '**', component: PageNotFoundComponent }
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
