#!/bin/python
from __future__ import annotations
from abc import ABC, abstractmethod

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy
import os
from rocket.model import BatchImport, BatchImportError, DBSession

import pandas as pd

from zipfile import ZipFile
from datetime import datetime

APPROOT = os.getcwd()
CODE_ROOT = os.path.join(APPROOT, "rocket")
PUBLIC_DIRNAME = os.path.join(CODE_ROOT, "public")
CSV_DIRNAME = os.path.join(PUBLIC_DIRNAME, 'csv')


# ***********************************************************************************
# Start of Command Pattern
# ***********************************************************************************

class Command(ABC):

    @abstractmethod
    def execute(self) -> None:
        pass


class ObjectStore:
    def __init__(self):
        self._store = {}

    def set_new_object(self, name: str, new_object) -> None:
        self._store.update({name: new_object})

    def get_object(self, name: str):
        return self._store.get(name, "No such object found")

    def show_objects(self) -> None:
        print(self._store)


class InitialImportReceiver:

    def __init__(self) -> None:
        self._batch_import_type_id = None
        self._batch_import_filename = ""
        self._batch_import_entity_id = None
        self._batch_import_processed_date = None
        self._batch_import_notes = ""

    def unzip(self, file_path, password=None) -> None:
        with ZipFile(file_path, 'r') as zipObj:
            if password:
                zipObj.extractall(pwd=bytes(password, 'utf-8'))
            else:
                zipObj.extractall()

    def set_batch_import_type_id(self, batch_import_type_id: int) -> None:  # TODO this will change with controllers
        self._batch_import_type_id = batch_import_type_id

    def set_batch_import_filename(self, batch_import_filename: str) -> None:
        self._batch_import_filename = batch_import_filename

    def set_batch_import_entity_id(self, batch_import_entity_id: int) -> None:  # TODO this will change with controllers
        self._batch_import_entity_id = batch_import_entity_id

    def set_batch_import_processed_date(self) -> None:
        self._batch_import_processed_date = datetime.now()

    def set_batch_import_notes(self, batch_import_notes: str) -> None:
        self._batch_import_notes = batch_import_notes

    def import_into_tbl_batch_import(self, object_store: ObjectStore):
        batch_import = BatchImport()
        batch_import.batch_import_type_id = self._batch_import_type_id
        batch_import.filename = self._batch_import_filename
        batch_import.entity_id = self._batch_import_entity_id
        batch_import.processed = self._batch_import_processed_date
        batch_import.notes = self._batch_import_notes
        DBSession.add(batch_import)
        DBSession.flush()
        object_store.set_new_object("batch_import_id", batch_import.id)


class MakeInitialImport(Command):

    def __init__(self, initial_import_receiver: InitialImportReceiver, object_store: ObjectStore, file_path: str,
                 import_type_id: int, password=None) -> None:
        self._initial_import_receiver = initial_import_receiver
        self._object_store = object_store
        self._file_path = file_path  # CSV_DIRNAME + '/' + 'LegalWiseImportData.zip'
        self._import_type_id = import_type_id
        self._password = password

        self._batch_import_type_id = self._import_type_id  # TODO this is temporary, when creating the method do so in the receiver class
        self._batch_import_filename = 'Member Import.csv'
        self._batch_import_entity_id = 1  # TODO this is temporary, when creating the method do so in the receiver class
        self._batch_import_notes = "Start"

    def execute(self) -> None:
        self._initial_import_receiver.unzip(self._file_path, password=self._password)
        self._initial_import_receiver.set_batch_import_type_id(self._batch_import_type_id)
        self._initial_import_receiver.set_batch_import_filename(self._batch_import_filename)
        self._initial_import_receiver.set_batch_import_entity_id(self._batch_import_entity_id)
        self._initial_import_receiver.set_batch_import_processed_date()
        self._initial_import_receiver.set_batch_import_notes(self._batch_import_notes)
        self._initial_import_receiver.import_into_tbl_batch_import(self._object_store)


class DataFrameReceiver:

    def __init__(self) -> None:
        self._import_file_name = None
        self._columns_from_import_file = []
        self._column_types = None
        self._column_dates = None
        self._new_column_names = None
        self._data_frame = None

    def set_import_file_name(self, import_file_name) -> None:
        self._import_file_name = CSV_DIRNAME + '/' + import_file_name  # TODO, fix this

    def set_columns_from_import_file(self, columns_from_import_file) -> None:
        self._columns_from_import_file = columns_from_import_file

    def set_column_types(self, column_types) -> None:
        self._column_types = column_types

    def set_column_dates(self, column_dates) -> None:
        self._column_dates = column_dates

    def set_new_column_names(self, new_column_names) -> None:
        self._new_column_names = new_column_names

    def make_data_frame_from_file(self) -> None:
        data = pd.read_excel(self._import_file_name, usecols=self._columns_from_import_file, dtype=self._column_types,
                             parse_dates=self._column_dates)
        data.rename(columns=self._new_column_names, inplace=True)
        self._data_frame = data

    def add_batch_import_id_to_data_frame(self, object_store: ObjectStore) -> None:
        self._data_frame['batch_import_id'] = object_store.get_object('batch_import_id')
        object_store.set_new_object("data_frame", self._data_frame)


class MakeDataFrame(Command):

    def __init__(self, data_frame_receiver: DataFrameReceiver, object_store: ObjectStore, import_filename) -> None:
        self._data_frame_receiver = data_frame_receiver
        self._object_store = object_store
        self. _import_file_name = import_filename

    _columns_from_import_file = ["IDNumber",
                                 "Name",
                                 "Surname",
                                 "MobileNumber",
                                 "Gender",
                                 "DOB(Ccyy-mm-dd)",
                                 "Language",
                                 "StartingDate (Ccyy-mm-dd)",
                                 "BeneficiaryIDNumber",
                                 'BeneficiaryDOB (Ccyy-mm-dd)',
                                 "BeneficiaryMobileNumber",
                                 "BeneficiaryFirstName",
                                 "BeneficiarySurname",
                                 "Relationship to Beneficiary",  # TODO this will have to be renamed to something else
                                 "IntermediaryCode",
                                 "GroupReference",
                                 "ProductCode"]
    _column_types = {"MobileNumber": "Int64",
                     "BeneficiaryMobileNumber": "Int64"}
    _new_column_names = {"IDNumber": 'identity_number',
                         "Name": 'first_name',
                         "Surname": "surname",
                         "MobileNumber": 'mobile',
                         "Gender": "gender",
                         "DOB(Ccyy-mm-dd)": "birthdate",
                         "Language": 'language',
                         "StartingDate (Ccyy-mm-dd)": 'startdate',
                         "BeneficiaryIDNumber": 'beneficiary_identity_number',
                         "BeneficiaryFirstName": 'beneficiary_first_name',
                         "BeneficiarySurname": 'beneficiary_surname',
                         "BeneficiaryMobileNumber": 'beneficiary_mobile',
                         'BeneficiaryDOB (Ccyy-mm-dd)': 'beneficiary_birthdate',
                         "GroupReference": "group_reference",
                         "IntermediaryCode": 'intermediary_code'}
    _column_dates = ["DOB(Ccyy-mm-dd)",
                     "StartingDate (Ccyy-mm-dd)",
                     'BeneficiaryDOB (Ccyy-mm-dd)']

    def execute(self) -> None:
        self._data_frame_receiver.set_import_file_name(self._import_file_name)
        self._data_frame_receiver.set_columns_from_import_file(self._columns_from_import_file)
        self._data_frame_receiver.set_column_types(self._column_types)
        self._data_frame_receiver.set_new_column_names(self._new_column_names)
        self._data_frame_receiver.set_column_dates(self._column_dates)
        self._data_frame_receiver.make_data_frame_from_file()
        self._data_frame_receiver.add_batch_import_id_to_data_frame(self._object_store)


class ConfirmationReceiver:

    def __init__(self) -> None:
        self._data_frame = None
        self._batch_import_id = None
        self._list_of_invalid_members = []
        self._list_of_invalid_beneficiaries = []
        self._batch_import_error_message = ""
        self._import_list = []

    def set_data_frame(self, _object_store: ObjectStore) -> None:
        self._data_frame = _object_store.get_object("data_frame")

    def set_batch_import_id(self, _object_store: ObjectStore) -> None:
        self._batch_import_id = _object_store.get_object("batch_import_id")

    def set_notes_on_tbl_batch_import_to_parse(self) -> None:
        batch_import = BatchImport.by_id(self._batch_import_id)
        batch_import.notes = "Start=>Parse"
        DBSession.flush()

    def get_and_set_list_of_invalid_members(self, object_store: ObjectStore) -> None:
        list_of_invalid_members = self._data_frame.loc[self._data_frame['first_name'].isnull() |
                                                       self._data_frame["surname"].isnull() |
                                                       self._data_frame['mobile'].isnull() |
                                                       self._data_frame['identity_number'].isnull()].index.tolist()
        self._list_of_invalid_members = list_of_invalid_members
        object_store.set_new_object("list_of_invalid_members", list_of_invalid_members)

    def get_and_set_list_of_invalid_beneficiaries(self, object_store: ObjectStore) -> None:
        list_of_invalid_beneficiaries = self._data_frame.loc[self._data_frame['beneficiary_first_name'].isnull() |
                                                             self._data_frame['beneficiary_surname'].isnull() |
                                                             self._data_frame['beneficiary_mobile'].isnull() |
                                                             self._data_frame['beneficiary_identity_number'].isnull()] \
            .index.tolist()
        list_of_empty_beneficiary = self._data_frame.loc[self._data_frame['beneficiary_first_name'].isnull() &
                                                         self._data_frame['beneficiary_surname'].isnull() &
                                                         self._data_frame['beneficiary_mobile'].isnull() &
                                                         self._data_frame['beneficiary_identity_number'].isnull()] \
            .index.tolist()
        list_of_invalid_beneficiaries = list(set(list_of_invalid_beneficiaries) - set(list_of_empty_beneficiary))
        self._list_of_invalid_beneficiaries = list_of_invalid_beneficiaries
        object_store.set_new_object("list_of_invalid_beneficiaries", sorted(list_of_invalid_beneficiaries))

    def set_batch_import_error_message(self, import_type: str, import_list: int) -> None:
        import_lists = {
            1: self._list_of_invalid_members,
            2: self._list_of_invalid_beneficiaries
        }
        self._batch_import_error_message = f"The following {import_type} are faulty {import_lists.get(import_list)}"

    def write_confirmation_results_to_tables(self) -> None:
        batch_import_error = BatchImportError()
        batch_import_error.batch_import_id = self._batch_import_id
        batch_import_error.message = self._batch_import_error_message
        DBSession.add(batch_import_error)
        DBSession.flush()


class MakeConfirmation(Command):

    def __init__(self, confirmation_receiver: ConfirmationReceiver, object_store: ObjectStore) -> None:
        self._confirmation_receiver = confirmation_receiver
        self._object_store = object_store

    def execute(self) -> None:
        self._confirmation_receiver.set_data_frame(self._object_store)
        self._confirmation_receiver.set_batch_import_id(self._object_store)
        self._confirmation_receiver.set_notes_on_tbl_batch_import_to_parse()
        self._confirmation_receiver.get_and_set_list_of_invalid_members(self._object_store)
        self._confirmation_receiver.get_and_set_list_of_invalid_beneficiaries(self._object_store)
        """Member Error"""
        self._confirmation_receiver.set_batch_import_error_message("Members", 1)
        self._confirmation_receiver.write_confirmation_results_to_tables()
        """Beneficiary Error"""
        self._confirmation_receiver.set_batch_import_error_message("Beneficiaries", 2)
        self._confirmation_receiver.write_confirmation_results_to_tables()


class ImportReceiver:

    def __init__(self) -> None:
        self._data_frame = None
        self._url = 'mysql://developer:developpass@localhost:3306/rocketdb'

    def set_data_frame(self, object_store: ObjectStore) -> None:
        self._data_frame = object_store.get_object("data_frame")

    def remove_erroneous_data_from_data_frame(self, object_store: ObjectStore) -> None:
        list_of_erroneous_entries = sorted(list(set(object_store.get_object("list_of_invalid_members") +
                                                    object_store.get_object("list_of_invalid_beneficiaries"))))
        self._data_frame = self._data_frame.drop(list_of_erroneous_entries, axis=0)
        object_store.set_new_object("cleaned_data_frame", self._data_frame)

    def set_notes_to_import(self, batch_import_id: int) -> None:
        batch_import = BatchImport.by_id(batch_import_id)
        batch_import.notes = "Start>Parse=>Import"
        DBSession.flush()

    def import_valid_data_into_data_base(self) -> None:
        engine = create_engine(self._url, echo=False)
        self._data_frame.drop(columns=['Relationship to Beneficiary', 'ProductCode'])\
            .to_sql('tbl_member_request', con=engine, if_exists='append', chunksize=1000, index=False)


class MakeImport(Command):

    def __init__(self, import_receiver: ImportReceiver, object_store: ObjectStore) -> None:
        self._import_receiver = import_receiver
        self._object_store = object_store

    def execute(self) -> None:
        self._import_receiver.set_data_frame(self._object_store)
        self._import_receiver.remove_erroneous_data_from_data_frame(self._object_store)
        self._import_receiver.set_notes_to_import(self._object_store.get_object('batch_import_id'))
        self._import_receiver.import_valid_data_into_data_base()


class BatchImportInvoker:
    _on_start = None
    _on_data_frame = None
    _on_confirmation = None
    _on_parse = None
    _on_import = None
    _on_complete = None

    def set_on_start(self, command: Command) -> None:
        self._on_start = command

    def set_on_data_frame(self, command: Command) -> None:
        self._on_data_frame = command

    def set_on_confirmation(self, command: Command) -> None:
        self._on_confirmation = command

    def set_on_parse(self, command: Command) -> None:
        self._on_parse = command

    def set_on_import(self, command: Command) -> None:
        self._on_import = command

    def set_on_complete(self, command: Command) -> None:
        self._on_complete = command

    def invoke(self) -> None:
        print("\n********************************************************")
        print(" <> Starting Batch Import Sequence <>")

        print("\nInitialising batch import")
        if isinstance(self._on_start, Command):
            self._on_start.execute()

        print("\nSetting up data frame")
        if isinstance(self._on_data_frame, Command):
            self._on_data_frame.execute()

        print("\nConfirming data validity")
        if isinstance(self._on_confirmation, Command):
            self._on_confirmation.execute()

        print("\nImporting data into database")
        if isinstance(self._on_import, Command):
            self._on_import.execute()
        #
        # print("Importing")
        # if isinstance(self._on_import, Command):
        #     self._on_import.execute()
        #
        # if isinstance(self._on_complete, Command):
        #     self._on_complete.execute()
        print("\n <> Completed Batch Import Sequence <>")
        print("********************************************************\n")


# MemberName = 'Member Import.csv'
# PurchaseName = 'Purchase Import.csv'

# pwd = "LW1mport"


# **************************************************************


# object_store = ObjectStore()
# batch_import_invoker = BatchImportInvoker()
#
# initial_import_receiver = InitialImportReceiver()
# batch_import_invoker.set_on_start(
# MakeInitialImport(initial_import_receiver, object_store, CSV_DIRNAME + '/' + 'LegalWiseImportData.zip', 1, "LW1mport"))
#
# data_frame_receiver = DataFrameReceiver()
# batch_import_invoker.set_on_data_frame(MakeDataFrame(data_frame_receiver, object_store, "Member Import.xlsx"))
#
# confirmation_receiver = ConfirmationReceiver()
# batch_import_invoker.set_on_confirmation((MakeConfirmation(confirmation_receiver, object_store)))
#
# import_receiver = ImportReceiver()
# batch_import_invoker.set_on_import(MakeImport(import_receiver, object_store))
#
# batch_import_invoker.invoke()


class CallToBatchImport:
    def __init__(self, file_name, import_type_id) -> None:
        self._object_store = ObjectStore()
        self._file_name = file_name
        self._import_type_id = int(import_type_id)

    def run_batch_import(self):
        batch_import_invoker = BatchImportInvoker()
        initial_import_receiver = InitialImportReceiver()
        try:
            batch_import_invoker.set_on_start(
                MakeInitialImport(initial_import_receiver, self._object_store,
                                  CSV_DIRNAME + '/' + 'LegalWiseImportData.zip', self._import_type_id, "LW1mport"))
        except Exception as e:
            print(e)
            return
        try:
            data_frame_receiver = DataFrameReceiver()
            batch_import_invoker.set_on_data_frame(MakeDataFrame(data_frame_receiver, self._object_store, self._file_name))
        except Exception as e:
            print(e)
            return
        try:
            confirmation_receiver = ConfirmationReceiver()
            batch_import_invoker.set_on_confirmation((MakeConfirmation(confirmation_receiver, self._object_store)))
        except Exception as e:
            print(e)
            return
        try:
            import_receiver = ImportReceiver()
            batch_import_invoker.set_on_import(MakeImport(import_receiver, self._object_store))
        except Exception as e:
            print(e)
            return
        try:
            batch_import_invoker.invoke()
        except Exception as e:
            print(e)
            return





# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
# object_store.show_objects()  # TODO this prints things
# print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
