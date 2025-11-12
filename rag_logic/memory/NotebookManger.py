from typing import Dict, List, Optional

from persistence.IxRepository.IRepos import INotebookRepository
from persistence.model.Notebook import Notebook
from persistence.mongo.MongoDBMS import MongoConnectionManager
from persistence.mongo.NotebookRepository import MongoNotebookRepository


class NotebookManager:
    counter = 0

    def __init__(self):
        self.notebook_dict: Dict[str, Notebook] = {}
        self.notebook_repo: INotebookRepository = MongoNotebookRepository(MongoConnectionManager.instance().db)

    def create_notebook(self, notebook_name: str, id_user: str) -> Notebook:
        """Crea un nuovo notebook e lo salva in memoria e su MongoDB"""
        NotebookManager.counter += 1
        notebook_name = notebook_name or f"Notebook{NotebookManager.counter}"
        notebook = Notebook(id_user=id_user, notebook_name=notebook_name)

        try:
            inserted_id = self.notebook_repo.create_notebook(notebook)
            notebook.id_notebook = inserted_id
            self.notebook_dict[notebook.id_notebook] = notebook
        except Exception as e:
            raise RuntimeError(f"Errore creando notebook: {e}")

        return notebook

    def delete_notebook(self, notebook_id: str):
        """Elimina un notebook da memoria e MongoDB"""

        self.notebook_dict.pop(notebook_id, None)
        try:
            deleted = self.notebook_repo.delete_notebook(notebook_id)
            if not deleted:
                raise RuntimeError(f"Notebook {notebook_id} non trovato nel DB")
        except Exception as e:
            raise RuntimeError(f"Errore cancellando notebook {notebook_id}: {e}")

    def update_notebook(self, notebook: Notebook):
        """Aggiorna un notebook esistente sia in memoria sia su MongoDB"""

        self.notebook_dict[notebook.id_notebook] = notebook
        try:
            self.notebook_repo.update_notebook(notebook)
        except Exception as e:
            raise RuntimeError(f"Errore aggiornando notebook {notebook.id_notebook}: {e}")

    def retrieve_notebook_by_id(self, notebook_id: str) -> Optional[Notebook]:
        """Recupera un notebook dalla memoria o dal DB"""

        if notebook_id in self.notebook_dict:
            return self.notebook_dict[notebook_id]

        try:
            data = self.notebook_repo.get_notebook_by_id(notebook_id)
            if data:
                notebook = Notebook.from_dict(data)
                self.notebook_dict[notebook_id] = notebook
                return notebook
        except Exception as e:
            raise RuntimeError(f"Errore recuperando notebook {notebook_id}: {e}")

        return None

    def retrieve_notebook_by_user(self, id_user: str) -> List[Notebook]:
        """Recupera tutti i notebook di un utente"""

        try:
            data_list = self.notebook_repo.get_notebook_by_user(id_user)
            notebooks = [Notebook.from_dict(d) for d in data_list]
            for nb in notebooks:
                self.notebook_dict[nb.id_notebook] = nb
            return notebooks
        except Exception as e:
            raise RuntimeError(f"Errore recuperando notebook per utente {id_user}: {e}")

    def update_metadata(self, notebook_id: str, last_chat_id: str, summary: str):
        """Aggiorna i metadata della chat di un notebook"""

        try:
            self.notebook_repo.update_chat_metadata(notebook_id, last_chat_id, summary)
        except Exception as e:
            raise RuntimeError(f"Errore aggiornando metadata del notebook {notebook_id}: {e}")

    def delete_metadata(self, notebook_id: str):
        """Elimina i metadata della chat di un notebook"""

        try:
            self.notebook_repo.delete_notebook(notebook_id)
        except Exception as e:
            raise RuntimeError(f"Errore eliminando metadata del notebook {notebook_id}: {e}")
