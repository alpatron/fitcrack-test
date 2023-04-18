"""Test data for test_encrypted_file.py"""
from __future__ import annotations
import pytest
from pathlib import Path

from .test_encrypted_file import EncryptedFileTestInput

TEST_DATA = [
    pytest.param(EncryptedFileTestInput(
        filepath=Path('./test/add_job_page_hash_input/encrypted_file/fc_auto_test_encrypted_file_rar4_encrypted_header.rar').absolute(),
        expected_hash='$RAR3$*0*1baaa857e88ceb60*71a3824ad520bce18d280f721c66425c',
        expected_hash_type='RAR3-hp'
    ), id='rar4_encrypted_header'),
    pytest.param(EncryptedFileTestInput(
        filepath=Path('./test/add_job_page_hash_input/encrypted_file/fc_auto_test_encrypted_file_rar4_unencrypted_header.rar').absolute(),
        expected_hash='$RAR3$*1*5fc854b69b709a8b*96d4119a*112*124*1*e7a7358b0a90b2c82693a99439c0ed6ded9be5c22a45de1d4b6c50fc1e26395309ffa5ea785777531e6fbaf829b0efe090a81d9678526b5ddbba841b126b26c7299b3f7b55543f26d1452b1107ed458bdc4ff92fa08ba38806dd07a43b19512997bc693670195d89585f021c00b9dbd6*33',
        expected_hash_type='RAR3-p (Compressed)'
    ), id='rar4_unencrypted_header'),
    pytest.param(EncryptedFileTestInput(
        filepath=Path('./test/add_job_page_hash_input/encrypted_file/fc_auto_test_encrypted_file_rar5_encrypted_header.rar').absolute(),
        expected_hash='$rar5$16$e87e114a354c975cf54b5c8c62ffdcfe$15$19614e86fef5a008cdc361070bd0d990$8$b032ca0fca03e85e',
        expected_hash_type='RAR5'
    ), id='rar5_encrypted_header'),
    pytest.param(EncryptedFileTestInput(
        filepath=Path('./test/add_job_page_hash_input/encrypted_file/fc_auto_test_encrypted_file_rar5_unencrypted_header.rar').absolute(),
        expected_hash='$rar5$16$2abc010d7e1b07b9520bd15ba01cdc4e$15$ebbdd9b1161f06f920b177aeefa510e4$8$88db240f538b27f7',
        expected_hash_type='RAR5'
    ), id='rar5_unencrypted_header'),
    pytest.param(EncryptedFileTestInput(
        filepath=Path('./test/add_job_page_hash_input/encrypted_file/fc_auto_test_encrypted_file_zip_new_encryption.zip').absolute(),
        expected_hash='$zip2$*0*3*0*3102d1a3b646d5e3b2bee78f6de78b0d*cad3*59*8283b4e5f986e8d0573fd8bcbda73e843909bc302d7b6ad6c561308610e9c44994024e8cff3614da3fee481f4f88d17b45105a6f750719d955650fe19f2b7b1c1485dee5ea68027a0f0cf651b05dc5ca36f2c3a1bd885390ff*c918bd9e93508eb50f58*$/zip2$',
        expected_hash_type='WinZip'
    ), id='zip_new_encryption'),
    pytest.param(EncryptedFileTestInput(
        filepath=Path('./test/add_job_page_hash_input/encrypted_file/fc_auto_test_encrypted_file_zip_old_encryption.zip').absolute(),
        expected_hash='$pkzip2$1*1*2*0*65*7c*9a11d496*0*3a*8*65*9a11*6677*41d58e7e4848a23073d79db6d9d9bddff8034f9a9f08bb305fb33a6ef2fc45ea1078a28dcdec30c7630db8e501dc4975896649ef7bf18c6e4a5a905b38d822a258e710c67a0e458951d3f7eb811dce8c560311b11b2d311dde3f2170a2bcacba67ef8d6f0f*$/pkzip2$',
        expected_hash_type='PKZIP (Compressed)'
    ), id='zip_old_encryption'),
    pytest.param(EncryptedFileTestInput(
        filepath=Path('./test/add_job_page_hash_input/encrypted_file/fc_auto_test_encrypted_file.7z').absolute(),
        expected_hash='$7z$2$19$0$$16$d7944c6e833bffcef528ea5c8470ddb6$2584859798$128$122$d7f4d467b184c5fa0ff7eacbe7d1116ed7277657efc342f4d3e21741d97565d40bed9cc211a72bab84424169f84e08827d7e3ca5fbfb865d847dce25918e83e48f9cdcb4b888f47c907c6a63d3216b3d0edba7ff52295091a69cffb67da6febeb4333c4ef25726523a131b5c6fb2008ba4caf28541cb6be09c41fc190957af14$124$00',
        expected_hash_type='7-Zip'
    ), id='7-zip'),
    pytest.param(EncryptedFileTestInput(
        filepath=Path('./test/add_job_page_hash_input/encrypted_file/fc_auto_test_encrypted_file.pdf').absolute(),
        expected_hash='$pdf$4*4*128*-3392*1*16*fa44424bbcb6b2110a0067458b6bc623*32*259621cdbd47625e9bc3eb197887171300000000000000000000000000000000*32*408b37bcf12da873d7f2840f3c1b917a023961ded4c8164d38e46e9655e66775',
        expected_hash_type='PDF 1.4 - 1.6 (Acrobat 5 - 8)'
    ), id='pdf'),
    pytest.param(EncryptedFileTestInput(
        filepath=Path('./test/add_job_page_hash_input/encrypted_file/fc_auto_test_encrypted_file.ppt').absolute(),
        expected_hash='$oldoffice$4*f1b3dfa9af28a14897ed4d6fc251b165*fc7bb3b48a9189e681d75144fbfba0e7*8a80d439bcfc40a2d86649abcbbbbab493bbbd18',
        expected_hash_type='MS Office <= 2003 $3/$4, SHA1 + RC4'
    ), id='MS_office_2003'),
    pytest.param(EncryptedFileTestInput(
        filepath=Path('./test/add_job_page_hash_input/encrypted_file/fc_auto_test_encrypted_file.pptx').absolute(),
        expected_hash='$office$*2013*100000*256*16*b47d2082a2644ff23d8dc71315451efb*96cc142e37f9ec3603b62cf8ffb1dbce*bbdbf799ab334483bd0c6b64efe50e23030183978d5acb1989559b8e7505c3b9',
        expected_hash_type='MS Office 2013'
    ), id='MS_office_2013')
]
