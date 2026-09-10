# Relevance Audit: Development Set

- Eval data: `evals\data\development.jsonl`
- Chunks: `corpus\processed\pytest-documentation\chunks.jsonl`
- Top k: `3`
- Items: 10
- Hits: 2
- Hit rate@3: 0.200

This report compares labeled relevant pages with retrieved pages.

## 1. dev-001: How do I use tmp_path to create temporary files in a test?

- Relevant pages: `[63]`
- Retrieved pages: `[77, 345, 472]`
- Hit: `False`

### Retrieved chunks

#### Rank 1: page 77, score 65.799, chunk `pytest-documentation-p0077-c01`

```text
pytest Documentation, Release 9.2 Otherpluginsmayaccessthe config.cacheobjecttoset/get json encodablevaluesbetweenpytestinvocations. INFO-CIRCLE Note Thispluginisenabledbydefault,butcanbedisabledifneeded: see Deactivating / unregistering a plugin by name(the internalnameforthispluginiscacheprovider). 2.9.2 Rerunning only failures or failures ﬁrst First,let’screate50testinvocationsofwhichonly2fail: # content of test_50.py import pytest @pytest.mark.parametrize("i", range(50)) def test_num(i): if i in (17, 25): pytest.fail("bad luck") Ifyourunthisforthefirsttimeyouwillseetwofailures: $ pytest -q .................F.......F........................ [100%] ================================= FAILURES ================================= _______________________________ test_num[17] _______________________________ i = 17 @pytest.mark.parametrize("i", range(50)) def test_num(i): if i in (17, 25): > py...
```

#### Rank 2: page 345, score 54.075, chunk `pytest-documentation-p0345-c01`

```text
pytest Documentation, Release 9.2 parseconfigure(*args) See Pytester.parseconfigure(). getitem(source, funcname='test_func') See Pytester.getitem(). getitems(source) See Pytester.getitems(). getmodulecol(source, configargs=(), withinit=False) See Pytester.getmodulecol(). collect_by_name(modcol, name) See Pytester.collect_by_name(). popen(cmdargs, stdout=-1, stderr=-1, stdin=NotSetType.token, **kw) See Pytester.popen(). run(*cmdargs, timeout=None, stdin=NotSetType.token) See Pytester.run(). runpython(script) See Pytester.runpython(). runpython_c(command) See Pytester.runpython_c(). runpytest_subprocess(*args, timeout=None) See Pytester.runpytest_subprocess(). spawn_pytest(string, expect_timeout=10.0) See Pytester.spawn_pytest(). spawn(cmd, expect_timeout=10.0) See Pytester.spawn(). tmp_path Tutorial: How to use temporary directories and files in tests tmp_path() Return a temporary directo...
```

#### Rank 3: page 472, score 52.995, chunk `pytest-documentation-p0472-c01`

```text
pytest Documentation, Release 9.2 (continuedfrompreviouspage) b = 2 > assert A.a == b, "A.a appears not to be b" E AssertionError: A.a appears not to be b E assert 1 == 2 E + where 1 = <class 'failure_demo.TestCustomAssertMsg.test_single_line. ˓→<locals>.A'>.a failure_demo.py:263: AssertionError ____________________ TestCustomAssertMsg.test_multiline ____________________ self = <failure_demo.TestCustomAssertMsg object at 0xdeadbeef002f> def test_multiline(self): class A: a = 1 b = 2 > assert A.a == b, ( "A.a appears not to be b\nor does not appear to be b\none of those" ) E AssertionError: A.a appears not to be b E or does not appear to be b E one of those E assert 1 == 2 E + where 1 = <class 'failure_demo.TestCustomAssertMsg.test_multiline.<locals> ˓→.A'>.a failure_demo.py:270: AssertionError ___________________ TestCustomAssertMsg.test_custom_repr ___________________ self = <failure_de...
```

### Labeled relevant page text

- Page 63: 2 chunk(s)
  - Chunk `pytest-documentation-p0063-c01`
```text
pytest Documentation, Release 9.2 Runningthiswouldresultinapassedtestexceptforthelastassert 0linewhichweusetolookatvalues: $ pytest test_tmp_path.py =========================== test session starts ============================ platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y rootdir: /home/sweet/project collected 1 item test_tmp_path.py F [100%] ================================= FAILURES ================================= _____________________________ test_create_file _____________________________ tmp_path = PosixPath('PYTEST_TMPDIR/test_create_file0') def test_create_file(tmp_path): d = tmp_path / "sub" d.mkdir() p = d / "hello.txt" p.write_text(CONTENT, encoding="utf-8") assert p.read_text(encoding="utf-8") == CONTENT assert len(list(tmp_path.iterdir())) == 1 > assert 0 E assert 0 test_tmp_path.py:11: AssertionError ========================= short test summary info ============...
```
  - Chunk `pytest-documentation-p0063-c02`
```text
tains the temporary directory for the last 3 pytest invocations. Concurrent invocations of the sametestfunctionaresupportedbyconfiguringthebasetemporarydirectorytobeuniqueforeachconcurrentrun. See temporary directory location and retentionfordetails. 2.6.2 The tmp_path_factory ﬁxture The tmp_path_factoryisasession-scopedfixturewhichcanbeusedtocreatearbitrarytemporarydirectoriesfrom anyotherfixtureortest. Forexample,supposeyourtestsuiteneedsalargeimageondisk,whichisgeneratedprocedurally. Insteadofcomputing thesameimageforeachtestthatusesitintoitsowntmp_path,youcangenerateitonceper-sessiontosavetime: # contents of conftest.py import pytest @pytest.fixture(scope="session") def image_file(tmp_path_factory): img = compute_expensive_image() fn = tmp_path_factory.mktemp("data") / "img.png" img.save(fn) return fn (continuesonnextpage) 2.6. How to use temporary directories and ﬁles in tests 59
```

## 2. dev-002: How can monkeypatch change environment variables during a test?

- Relevant pages: `[65, 69]`
- Retrieved pages: `[65, 69, 65]`
- Hit: `True`

### Retrieved chunks

#### Rank 1: page 65, score 97.665, chunk `pytest-documentation-p0065-c02`

```text
distributingtestsonthelocalmachineusingpytest-xdist,careistakentoautomaticallyconfigureabasetemp directoryforthesubprocessessuchthatalltemporarydatalandsbelowasingleper-testruntemporarydirectory. 2.7 How to monkeypatch/mock modules and environments Sometimes tests need to invoke functionality which depends on global settings or which invokes code which cannot be easilytestedsuchasnetworkaccess. Themonkeypatchfixturehelpsyoutosafelyset/deleteanattribute,dictionaryitem orenvironmentvariable,ortomodifysys.pathforimporting. Themonkeypatchfixtureprovidesthesehelpermethodsforsafelypatchingandmockingfunctionalityintests: • monkeypatch.setattr(obj, name, value, raising=True) • monkeypatch.delattr(obj, name, raising=True) • monkeypatch.setitem(mapping, name, value) • monkeypatch.delitem(obj, name, raising=True) • monkeypatch.setenv(name, value, prepend=None) • monkeypatch.delenv(name, raising=Tru...
```

#### Rank 2: page 69, score 71.427, chunk `pytest-documentation-p0069-c01`

```text
pytest Documentation, Release 9.2 import functools def test_partial(monkeypatch): with monkeypatch.context() as m: m.setattr(functools, "partial", 3) assert functools.partial == 3 See#3290fordetails. 2.7.4 Monkeypatching environment variables Ifyouareworkingwithenvironmentvariablesyouoftenneedtosafelychangethevaluesordeletethemfromthesystem for testing purposes. monkeypatch provides a mechanism to do this using the setenv and delenv method. Our examplecodetotest: # contents of our original code file e.g. code.py import os def get_os_user_lower(): """Simple retrieval function. Returns lowercase USER or raises OSError.""" username = os.getenv("USER") if username is None: raise OSError("USER environment is not set.") return username.lower() There are two potential paths. First, the USER environment variable is set to a value. Second, the USER environment variabledoesnotexist. Usingmonkeypat...
```

#### Rank 3: page 65, score 62.131, chunk `pytest-documentation-p0065-c03`

```text
setitem to patch the dictionary for the test. monkeypatch.delitem can be used to remove items. 3. Modifying environment variables for a test e.g. to test program behavior if an environment variable is missing, or tosetmultiplevaluestoaknownvariable. monkeypatch.setenv and monkeypatch.delenv canbeusedforthese patches. 4. Usemonkeypatch.setenv("PATH", value, prepend=os.pathsep)tomodify$PATH,and monkeypatch. chdir tochangethecontextofthecurrentworkingdirectoryduringatest. 5. Use monkeypatch.syspath_prepend to modify sys.path which will also call pkg_resources. fixup_namespace_packagesandimportlib.invalidate_caches(). 6. Use monkeypatch.contexttoapplypatchesonlyinaspecificscope,whichcanhelpcontrolteardownofcomplex fixturesorpatchestothestdlib. Seethemonkeypatchblogpostforsomeintroductionmaterialandadiscussionofitsmotivation. 2.7. How to monkeypatch/mock modules and environments 61
```

### Labeled relevant page text

- Page 65: 3 chunk(s)
  - Chunk `pytest-documentation-p0065-c01`
```text
pytest Documentation, Release 9.2 Exclamation-Triangle Warning Thedirectorygivento --basetempwillbeclearedblindlybeforeeachtestrun,somakesuretouseadirectory forthatpurposeonly. Whendistributingtestsonthelocalmachineusingpytest-xdist,careistakentoautomaticallyconfigureabasetemp directoryforthesubprocessessuchthatalltemporarydatalandsbelowasingleper-testruntemporarydirectory. 2.7 How to monkeypatch/mock modules and environments
```
  - Chunk `pytest-documentation-p0065-c02`
```text
distributingtestsonthelocalmachineusingpytest-xdist,careistakentoautomaticallyconfigureabasetemp directoryforthesubprocessessuchthatalltemporarydatalandsbelowasingleper-testruntemporarydirectory. 2.7 How to monkeypatch/mock modules and environments Sometimes tests need to invoke functionality which depends on global settings or which invokes code which cannot be easilytestedsuchasnetworkaccess. Themonkeypatchfixturehelpsyoutosafelyset/deleteanattribute,dictionaryitem orenvironmentvariable,ortomodifysys.pathforimporting. Themonkeypatchfixtureprovidesthesehelpermethodsforsafelypatchingandmockingfunctionalityintests: • monkeypatch.setattr(obj, name, value, raising=True) • monkeypatch.delattr(obj, name, raising=True) • monkeypatch.setitem(mapping, name, value) • monkeypatch.delitem(obj, name, raising=True) • monkeypatch.setenv(name, value, prepend=None) • monkeypatch.delenv(name, raising=Tru...
```
  - Chunk `pytest-documentation-p0065-c03`
```text
setitem to patch the dictionary for the test. monkeypatch.delitem can be used to remove items. 3. Modifying environment variables for a test e.g. to test program behavior if an environment variable is missing, or tosetmultiplevaluestoaknownvariable. monkeypatch.setenv and monkeypatch.delenv canbeusedforthese patches. 4. Usemonkeypatch.setenv("PATH", value, prepend=os.pathsep)tomodify$PATH,and monkeypatch. chdir tochangethecontextofthecurrentworkingdirectoryduringatest. 5. Use monkeypatch.syspath_prepend to modify sys.path which will also call pkg_resources. fixup_namespace_packagesandimportlib.invalidate_caches(). 6. Use monkeypatch.contexttoapplypatchesonlyinaspecificscope,whichcanhelpcontrolteardownofcomplex fixturesorpatchestothestdlib. Seethemonkeypatchblogpostforsomeintroductionmaterialandadiscussionofitsmotivation. 2.7. How to monkeypatch/mock modules and environments 61
```

- Page 69: 1 chunk(s)
  - Chunk `pytest-documentation-p0069-c01`
```text
pytest Documentation, Release 9.2 import functools def test_partial(monkeypatch): with monkeypatch.context() as m: m.setattr(functools, "partial", 3) assert functools.partial == 3 See#3290fordetails. 2.7.4 Monkeypatching environment variables Ifyouareworkingwithenvironmentvariablesyouoftenneedtosafelychangethevaluesordeletethemfromthesystem for testing purposes. monkeypatch provides a mechanism to do this using the setenv and delenv method. Our examplecodetotest: # contents of our original code file e.g. code.py import os def get_os_user_lower(): """Simple retrieval function. Returns lowercase USER or raises OSError.""" username = os.getenv("USER") if username is None: raise OSError("USER environment is not set.") return username.lower() There are two potential paths. First, the USER environment variable is set to a value. Second, the USER environment variabledoesnotexist. Usingmonkeypat...
```

## 3. dev-003: How do I parametrize a test function with multiple examples?

- Relevant pages: `[48, 493]`
- Retrieved pages: `[511, 77, 498]`
- Hit: `False`

### Retrieved chunks

#### Rank 1: page 511, score 79.993, chunk `pytest-documentation-p0511-c01`

```text
pytest Documentation, Release 9.2 (continuedfrompreviouspage) @pytest.mark.skip(reason=None): skip the given test function with an optional reason.␣ ˓→Example: skip(reason="no way of currently testing this") skips the test. @pytest.mark.skipif(condition, ..., *, reason=...): skip the given test function if␣ ˓→any of the conditions evaluate to True. Example: skipif(sys.platform == 'win32')␣ ˓→skips the test if we are on the win32 platform. See https://docs.pytest.org/en/ ˓→stable/reference/reference.html#pytest-mark-skipif @pytest.mark.xfail(condition, ..., *, reason=..., run=True, raises=None,␣ ˓→strict=strict_xfail): mark the test function as an expected failure if any of the␣ ˓→conditions evaluate to True. Optionally specify a reason for better reporting and␣ ˓→run=False if you don't even want to execute the test function. If only specific␣ ˓→exception(s) are expected, you can list the...
```

#### Rank 2: page 77, score 66.781, chunk `pytest-documentation-p0077-c01`

```text
pytest Documentation, Release 9.2 Otherpluginsmayaccessthe config.cacheobjecttoset/get json encodablevaluesbetweenpytestinvocations. INFO-CIRCLE Note Thispluginisenabledbydefault,butcanbedisabledifneeded: see Deactivating / unregistering a plugin by name(the internalnameforthispluginiscacheprovider). 2.9.2 Rerunning only failures or failures ﬁrst First,let’screate50testinvocationsofwhichonly2fail: # content of test_50.py import pytest @pytest.mark.parametrize("i", range(50)) def test_num(i): if i in (17, 25): pytest.fail("bad luck") Ifyourunthisforthefirsttimeyouwillseetwofailures: $ pytest -q .................F.......F........................ [100%] ================================= FAILURES ================================= _______________________________ test_num[17] _______________________________ i = 17 @pytest.mark.parametrize("i", range(50)) def test_num(i): if i in (17, 25): > py...
```

#### Rank 3: page 498, score 50.053, chunk `pytest-documentation-p0498-c01`

```text
pytest Documentation, Release 9.2 Parametrizing test methods through per-class conﬁguration Here is an example pytest_generate_tests function implementing a parametrization scheme similar to Michael Foord’sunittestparametrizerbutinalotlesscode: # content of ./test_parametrize.py import pytest def pytest_generate_tests(metafunc): # called once per each test function funcarglist = metafunc.cls.params[metafunc.function.__name__] argnames = sorted(funcarglist[0]) metafunc.parametrize( argnames, [[funcargs[name] for name in argnames] for funcargs in funcarglist] ) class TestClass: # a map specifying multiple argument sets for a test method params = { "test_equals": [dict(a=1, b=2), dict(a=3, b=3)], "test_zerodivision": [dict(a=1, b=0)], } def test_equals(self, a, b): assert a == b def test_zerodivision(self, a, b): with pytest.raises(ZeroDivisionError): a / b Ourtestgeneratorlooksupaclass-lev...
```

### Labeled relevant page text

- Page 48: 1 chunk(s)
  - Chunk `pytest-documentation-p0048-c01`
```text
pytest Documentation, Release 9.2 (continuedfrompreviouspage) def test_b(b): pass Theaboveshowshow idscanbeeitheralistofstringstouseorafunctionwhichwillbecalledwiththefixturevalue andthenhastoreturnastringtouse. InthelattercaseifthefunctionreturnsNonethenpytest’sauto-generatedIDwill beused. RunningtheabovetestsresultsinthefollowingtestIDsbeingused: $ pytest --collect-only =========================== test session starts ============================ platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y rootdir: /home/sweet/project collected 12 items <Dir fixtures.rst-236> <Module test_anothersmtp.py> <Function test_showhelo[smtp.gmail.com]> <Function test_showhelo[mail.python.org]> <Module test_emaillib.py> <Function test_email_received> <Module test_finalizers.py> <Function test_bar> <Module test_ids.py> <Function test_a[spam]> <Function test_a[ham]> <Function test_b[eggs]> <Function...
```

- Page 493: 2 chunk(s)
  - Chunk `pytest-documentation-p0493-c01`
```text
pytest Documentation, Release 9.2 (continuedfrompreviouspage) ), ], ) def test_timedistance_v3(a, b, expected): diff = a - b assert diff == expected Intest_timedistance_v0,weletpytestgeneratethetestIDs. Intest_timedistance_v1,wespecifiedidsasalistofstringswhichwereusedasthetestIDs. Thesearesuccinct, butcanbeapaintomaintain. Intest_timedistance_v2,wespecifiedidsasafunctionthatcangenerateastringrepresentationtomakepartofthe testID.Soourdatetimevaluesusethelabelgeneratedbyidfn,butbecausewedidn’tgeneratealabelfortimedelta objects,theyarestillusingthedefaultpytestrepresentation: $ pytest test_time.py --collect-only =========================== test session starts ============================ platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y rootdir: /home/sweet/project collected 8 items <Dir parametrize.rst-215> <Module test_time.py> <Function test_timedistance_v0[a0-b0-expected0]> <F...
```
  - Chunk `pytest-documentation-p0493-c02`
```text
Here is a quick port to run tests configured with testscenarios, an add-on from Robert Collins for the standard unittest framework. Weonlyhavetoworkabittoconstructthecorrectargumentsforpytest’s Metafunc.parametrize: # content of test_scenarios.py def pytest_generate_tests(metafunc): idlist = [] argvalues = [] for scenario in metafunc.cls.scenarios: idlist.append(scenario[0]) items = scenario[1].items() argnames = [x[0] for x in items] argvalues.append([x[1] for x in items]) (continuesonnextpage) 5.1. Examples and customization tricks 489
```

## 4. dev-004: How do pytest fixtures share setup between tests?

- Relevant pages: `[112, 121]`
- Retrieved pages: `[14, 184, 123]`
- Hit: `False`

### Retrieved chunks

#### Rank 1: page 14, score 45.033, chunk `pytest-documentation-p0014-c01`

```text
pytest Documentation, Release 9.2 pytest tests/test_mod.py::TestClass Specifyingaspecifictestmethod: pytest tests/test_mod.py::TestClass::test_method Specifyingaspecificparametrizationofatest: pytest tests/test_mod.py::test_func[x1,y2] Run tests by marker expressions Torunalltestswhicharedecoratedwiththe@pytest.mark.slowdecorator: pytest -m slow To run all tests which are decorated with the annotated @pytest.mark.slow(phase=1) decorator, with the phase keywordargumentsetto1: pytest -m "slow(phase=1)" Formoreinformationsee marks. Run tests from packages pytest --pyargs pkg.testing Thiswillimportpkg.testinganduseitsfilesystemlocationtofindandruntestsfrom. Read arguments from file Addedinversion8.2. Alloftheabovecanbereadfromafileusingthe@prefix: pytest @tests_to_run.txt wheretests_to_run.txtcontainsanentryperline,e.g.: tests/test_file.py tests/test_mod.py::test_func[x1,y2] tests/test_mod.p...
```

#### Rank 2: page 184, score 44.445, chunk `pytest-documentation-p0184-c02`

```text
pytest Documentation, Release 9.2 pytest-docker-db last release: Mar20,2021, status: 5-Production/Stable, requires: pytest(>=3.1.1) Aplugintousedockerdatabasesforpytests pytest-docker-fixtures last release: May07,2026, status: 3-Alpha, requires: pytest pytestdockerfixtures pytest-docker-git-fixtures last release: Aug12,2024, status: 4-Beta, requires: pytest Pytestfixturesfortestingwithgitscm. pytest-docker-haproxy-fixtures last release: Aug12,2024, status: 4-Beta, requires: pytest Pytestfixturesfortestingwithhaproxy. pytest-docker-pexpect last release: Jan14,2019, status: N/A, requires: pytest pytestpluginforwritingfunctionaltestswithpexpectanddocker pytest-docker-postgresql last release: Sep24,2019, status: 4-Beta, requires: pytest(>=3.5.0) Asimpleplugintousewithpytest pytest-docker-py last release: Nov27,2018, status: N/A, requires: pytest(==4.0.0) Easytouse,simpletoextend,pytestplugin...
```

#### Rank 3: page 123, score 42.782, chunk `pytest-documentation-p0123-c01`

```text
pytest Documentation, Release 9.2 (continuedfrompreviouspage) """teardown any state that was previously setup with a setup_module method. """ Asofpytest-3.0,themoduleparameterisoptional. 2.19.2 Class level setup/teardown Similarly,thefollowingmethodsarecalledatclasslevelbeforeandafteralltestmethodsoftheclassarecalled: @classmethod def setup_class(cls): """setup any state specific to the execution of the given class (which usually contains tests). """ @classmethod def teardown_class(cls): """teardown any state that was previously setup with a call to setup_class. """ 2.19.3 Method and function level setup/teardown Similarly,thefollowingmethodsarecalledaroundeachmethodinvocation: def setup_method(self, method): """setup any state tied to the execution of the given method in a class. setup_method is invoked for every test method of a class. """ def teardown_method(self, method): """teardown...
```

### Labeled relevant page text

- Page 112: 2 chunk(s)
  - Chunk `pytest-documentation-p0112-c01`
```text
pytest Documentation, Release 9.2 (continuedfrompreviouspage) def test_example(): pass $ pytest =========================== test session starts ============================ platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y rootdir: /home/sweet/project configfile: pytest.toml collected 2 items test_example.py .. [100%] ============================ 2 passed in 0.12s ============================= Formoreinformationabouttheresultobjectthatrunpytest()returns,andthemethodsthatitprovidespleasecheck outthe RunResultdocumentation. 2.16 Writing hook functions 2.16.1 hook function validation and execution pytestcallshookfunctionsfromregisteredpluginsforanygivenhookspecification. Let’slookatatypicalhookfunction forthepytest_collection_modifyitems(session, config, items)hookwhichpytestcallsaftercollection ofalltestitemsiscompleted. Whenweimplementapytest_collection_modifyitemsfunctioninourpl...
```
  - Chunk `pytest-documentation-p0112-c02`
```text
ters without breaking the signatures of existinghookimplementations. Itisoneofthereasonsforthegenerallong-livedcompatibilityofpytestplugins. Notethathookfunctionsotherthan pytest_runtest_*arenotallowedtoraiseexceptions. Doingsowillbreakthe pytestrun. 2.16.2 ﬁrstresult: stop at ﬁrst non-None result Mostcallstopytesthooksresultina list of resultswhichcontainsallnon-Noneresultsofthecalledhookfunctions. Some hook specifications use the firstresult=True option so that the hook call only executes until the first of N registeredfunctionsreturnsanon-Noneresultwhichisthentakenasresultoftheoverallhookcall. Theremaininghook functionswillnotbecalledinthiscase. 108 Chapter 2. How-to guides
```

- Page 121: 2 chunk(s)
  - Chunk `pytest-documentation-p0121-c01`
```text
pytest Documentation, Release 9.2 (continuedfrompreviouspage) > assert 0, self.db # fail for demo purposes ^^^^^^^^^^^^^^^^^ E AssertionError: <conftest.db_class.<locals>.DummyDB object at 0xdeadbeef0001> E assert 0 test_unittest_db.py:11: AssertionError ___________________________ MyTest.test_method2 ____________________________ self = <test_unittest_db.MyTest testMethod=test_method2> def test_method2(self): > assert 0, self.db # fail for demo purposes ^^^^^^^^^^^^^^^^^ E AssertionError: <conftest.db_class.<locals>.DummyDB object at 0xdeadbeef0001> E assert 0 test_unittest_db.py:14: AssertionError ========================= short test summary info ========================== FAILED test_unittest_db.py::MyTest::test_method1 - AssertionError: <conft... FAILED test_unittest_db.py::MyTest::test_method2 - AssertionError: <conft... ============================ 2 failed in 0.12s ================...
```
  - Chunk `pytest-documentation-p0121-c02`
```text
ssertionError: <conft... ============================ 2 failed in 0.12s ============================= Thisdefaultpytesttracebackshowsthatthetwotestmethodssharethesameself.dbinstancewhichwasourintention whenwritingtheclass-scopedfixturefunctionabove. 2.18.4 Using autouse ﬁxtures and accessing other ﬁxtures Althoughit’susuallybettertoexplicitlydeclareuseoffixturesyouneedforagiventest,youmaysometimeswanttohave fixturesthatareautomaticallyusedinagivencontext. Afterall, thetraditionalstyleofunittest-setupmandatestheuse ofthisimplicitfixturewritingandchancesare,youareusedtoitorlikeit. Youcanflagfixturefunctionswith@pytest.fixture(autouse=True)anddefinethefixturefunctioninthecontext where you want it used. Let’s look at an initdir fixture which makes all test methods of a TestCase class execute in a temporary directory with a pre-initialized samplefile.ini. Our initdir fixture itself uses the p...
```

## 5. dev-005: How do I skip a test or mark it xfail?

- Relevant pages: `[511]`
- Retrieved pages: `[511, 507, 97]`
- Hit: `True`

### Retrieved chunks

#### Rank 1: page 511, score 87.437, chunk `pytest-documentation-p0511-c01`

```text
pytest Documentation, Release 9.2 (continuedfrompreviouspage) @pytest.mark.skip(reason=None): skip the given test function with an optional reason.␣ ˓→Example: skip(reason="no way of currently testing this") skips the test. @pytest.mark.skipif(condition, ..., *, reason=...): skip the given test function if␣ ˓→any of the conditions evaluate to True. Example: skipif(sys.platform == 'win32')␣ ˓→skips the test if we are on the win32 platform. See https://docs.pytest.org/en/ ˓→stable/reference/reference.html#pytest-mark-skipif @pytest.mark.xfail(condition, ..., *, reason=..., run=True, raises=None,␣ ˓→strict=strict_xfail): mark the test function as an expected failure if any of the␣ ˓→conditions evaluate to True. Optionally specify a reason for better reporting and␣ ˓→run=False if you don't even want to execute the test function. If only specific␣ ˓→exception(s) are expected, you can list the...
```

#### Rank 2: page 507, score 82.440, chunk `pytest-documentation-p0507-c01`

```text
pytest Documentation, Release 9.2 (continuedfrompreviouspage) cachedir: .pytest_cache rootdir: /home/sweet/project collecting ... collected 4 items / 2 deselected / 2 selected test_server.py::test_send_http PASSED [ 50%] test_server.py::test_something_quick PASSED [100%] ===================== 2 passed, 2 deselected in 0.12s ====================== Youcanuseand,or,notandparentheses. Inadditiontothetest’sname, -kalsomatchesthenamesofthetest’sparents(usually,thenameofthefileandclassit’s in),attributessetonthetestfunction,markersappliedtoitoritsparentsandany extra keywordsexplicitlyaddedto itoritsparents. Registering markers Registeringmarkersforyourtestsuiteissimple: # content of pytest.toml [pytest] markers = ["webtest: mark a test as a webtest.", "slow: mark test as slow."] Multiplecustommarkerscanberegistered,bydefiningeachoneinitsownline,asshowninaboveexample. Youcanaskwhichmarkersexistf...
```

#### Rank 3: page 97, score 67.960, chunk `pytest-documentation-p0097-c01`

```text
pytest Documentation, Release 9.2 pytestcountsandlists skipand xfail testsseparately. Detailedinformationaboutskipped/xfailedtestsisnotshownby defaulttoavoidclutteringtheoutput. Youcanusethe -roptiontoseedetailscorrespondingtothe“short”lettersshown inthetestprogress: pytest -rxXs # show extra info on xfailed, xpassed, and skipped tests Moredetailsonthe -r optioncanbefoundbyrunningpytest -h. (See Builtin configuration file options) 2.13.1 Skipping test functions Thesimplestwaytoskipatestfunctionistomarkitwiththeskipdecoratorwhichmaybepassedanoptionalreason: @pytest.mark.skip(reason="no way of currently testing this") def test_the_unknown(): ... Alternatively,itisalsopossibletoskipimperativelyduringtestexecutionorsetupbycallingthepytest.skip(reason) function: def test_function(): if not valid_config(): pytest.skip("unsupported configuration") Theimperativemethodisusefulwhenitisnotpossiblet...
```

### Labeled relevant page text

- Page 511: 2 chunk(s)
  - Chunk `pytest-documentation-p0511-c01`
```text
pytest Documentation, Release 9.2 (continuedfrompreviouspage) @pytest.mark.skip(reason=None): skip the given test function with an optional reason.␣ ˓→Example: skip(reason="no way of currently testing this") skips the test. @pytest.mark.skipif(condition, ..., *, reason=...): skip the given test function if␣ ˓→any of the conditions evaluate to True. Example: skipif(sys.platform == 'win32')␣ ˓→skips the test if we are on the win32 platform. See https://docs.pytest.org/en/ ˓→stable/reference/reference.html#pytest-mark-skipif @pytest.mark.xfail(condition, ..., *, reason=..., run=True, raises=None,␣ ˓→strict=strict_xfail): mark the test function as an expected failure if any of the␣ ˓→conditions evaluate to True. Optionally specify a reason for better reporting and␣ ˓→run=False if you don't even want to execute the test function. If only specific␣ ˓→exception(s) are expected, you can list the...
```
  - Chunk `pytest-documentation-p0511-c02`
```text
/docs.pytest.org/en/stable/how-to/parametrize.html for more info␣ ˓→and examples. @pytest.mark.usefixtures(fixturename1, fixturename2, ...): mark tests as needing all␣ ˓→of the specified fixtures. see https://docs.pytest.org/en/stable/explanation/ ˓→fixtures.html#usefixtures @pytest.mark.tryfirst: mark a hook implementation function such that the plugin␣ ˓→machinery will try to call it first/as early as possible. DEPRECATED, use @pytest. ˓→hookimpl(tryfirst=True) instead. @pytest.mark.trylast: mark a hook implementation function such that the plugin␣ ˓→machinery will try to call it last/as late as possible. DEPRECATED, use @pytest. ˓→hookimpl(trylast=True) instead. Passing a callable to custom markers Belowistheconfigfilethatwillbeusedinthenextexamples: # content of conftest.py import sys def pytest_runtest_setup(item): for marker in item.iter_markers(name="my_marker"): print(marker) sys...
```

## 6. dev-006: How does pytest discover configuration from pytest.ini?

- Relevant pages: `[189, 190]`
- Retrieved pages: `[305, 181, 286]`
- Hit: `False`

### Retrieved chunks

#### Rank 1: page 305, score 72.821, chunk `pytest-documentation-p0305-c02`

```text
pytest Documentation, Release 9.2 Finding the rootdir Hereisthealgorithmwhichfindstherootdirfromargs: • If -cispassedinthecommand-line,usethatasconfigurationfile,anditsdirectoryasrootdir. • Determinethecommonancestordirectoryforthespecifiedargsthatarerecognisedaspathsthatexistinthefile system. Ifnosuchpathsarefound,thecommonancestordirectoryissettothecurrentworkingdirectory. • Look for pytest.toml, .pytest.toml, pytest.ini, .pytest.ini, pyproject.toml, tox.ini, and setup.cfg files in the ancestor directory and upwards. If one is matched, it becomes the configfile and itsdirectorybecomestherootdir. • Ifnoconfigurationfilewasfound,lookforsetup.pyupwardsfromthecommonancestordirectorytodetermine therootdir. • If no setup.py was found, look for pytest.toml, .pytest.toml, pytest.ini, .pytest.ini, pyproject.toml,tox.ini,andsetup.cfgineachofthespecifiedargsandupwards. Ifoneismatched,it becomesth...
```

#### Rank 2: page 181, score 72.656, chunk `pytest-documentation-p0181-c02`

```text
pytest Documentation, Release 9.2 pytest-dir-equalsisapytestpluginprovidinghelperstoassertdirectoriesequalityallowinggoldentesting pytest-dirty last release: Jun08,2025, status: 3-Alpha, requires: pytest>=8.2;extra==“dev” Staticimportanalysisforthriftytesting. pytest-disable last release: Sep10,2015, status: 4-Beta, requires: N/A pytestplugintodisableatestandskipitfromtestrun pytest-disable-plugin last release: Feb28,2019, status: 4-Beta, requires: pytest(>=3.5.0) Disablepluginspertest pytest-discord last release: May11,2024, status: 4-Beta, requires: pytest!=6.0.0,<9,>=3.3.2 ApytestplugintonotifytestresultstoaDiscordchannel. pytest-discover last release: Mar26,2024, status: N/A, requires: pytest Pytestplugintorecorddiscoveredtestsinafile pytest-ditto last release: Mar22,2026, status: 5-Production/Stable, requires: pytest>=3.5.0 Snapshottestingpytestpluginwithminimalceremonyandflexiblere...
```

#### Rank 3: page 286, score 67.708, chunk `pytest-documentation-p0286-c02`

```text
pytest Documentation, Release 9.2 pytest-testrail-ns last release: Aug12,2022, status: N/A, requires: N/A pytestpluginforcreatingTestRailrunsandaddingresults pytest-testrail-reporter last release: Sep10,2018, status: N/A, requires: N/A pytest-testrail-results last release: Mar04,2024, status: N/A, requires: pytest>=7.2.0 ApytestplugintouploadresultstoTestRail. pytest-testreport last release: Dec01,2022, status: 4-Beta, requires: pytest(>=3.5.0) pytest-testreport-new last release: Oct07,2023, status: 4-Beta, requires: pytest>=3.5.0 pytest-testslide last release: Jan07,2021, status: 5-Production/Stable, requires: pytest(~=6.2) TestSlidefixtureforpytest pytest-test-this last release: Sep15,2019, status: 2-Pre-Alpha, requires: pytest(>=2.3) Plugin forpy.test to run relevanttests, based on naivelychecking ifa testcontains a reference to the symbol you supply pytest-test-tracer-for-pytest last...
```

### Labeled relevant page text

- Page 189: 2 chunk(s)
  - Chunk `pytest-documentation-p0189-c01`
```text
pytest Documentation, Release 9.2
```
  - Chunk `pytest-documentation-p0189-c02`
```text
pytest Documentation, Release 9.2 pytest-elk-reporter last release: Jul25,2024, status: 4-Beta, requires: pytest>=3.5.0 Asimpleplugintousewithpytest pytest-email last release: Jul08,2020, status: N/A, requires: pytest Sendexecutionresultemail pytest-embedded last release: Aug31,2026, status: 5-Production/Stable, requires: pytest>=7.0 Apytestpluginthatdesignedforembeddedtesting. pytest-embedded-arduino last release: Aug31,2026, status: 5-Production/Stable, requires: N/A Makepytest-embeddedpluginworkwithArduino. pytest-embedded-arduino-cli last release: Aug14,2026, status: N/A, requires: pytest>=8 ApytestplugintotestArduinoprojectsusingpytest-embeddedandarduino-cli pytest-embedded-espemu last release: Aug31,2026, status: 4-Beta, requires: N/A Makepytest-embeddedpluginworkwithesp-emu. pytest-embedded-idf last release: Aug31,2026, status: 5-Production/Stable, requires: N/A Makepytest-embedde...
```

- Page 190: 2 chunk(s)
  - Chunk `pytest-documentation-p0190-c01`
```text
pytest Documentation, Release 9.2
```
  - Chunk `pytest-documentation-p0190-c02`
```text
pytest Documentation, Release 9.2 pytest-embrace last release: Mar25,2023, status: N/A, requires: pytest(>=7.0,<8.0) 💝Dataclasses-as-tests. Describetheruntimeonceandmultiplycoveragewithnoboilerplate. pytest-emoji last release: Feb19,2019, status: 4-Beta, requires: pytest(>=4.2.1) Apytestpluginthataddsemojistoyourtestresultreport pytest-emoji-output last release: Apr09,2023, status: 4-Beta, requires: pytest(==7.0.1) Pytestplugintorepresenttestoutputwithemojisupport pytest-enabler last release: May16,2025, status: 5-Production/Stable, requires: pytest!=8.1.*,>=6;extra==“test” Enableinstalledpytestplugins pytest-encode last release: Nov06,2021, status: N/A, requires: N/A setyourencodingandlogger pytest-encode-kane last release: Nov16,2021, status: N/A, requires: pytest setyourencodingandlogger pytest-encoding last release: Aug11,2023, status: N/A, requires: pytest setyourencodingandlogger p...
```

## 7. dev-007: How can I capture stdout and stderr in pytest?

- Relevant pages: `[149, 150]`
- Retrieved pages: `[87, 77, 324]`
- Hit: `False`

### Retrieved chunks

#### Rank 1: page 87, score 77.686, chunk `pytest-documentation-p0087-c01`

```text
pytest Documentation, Release 9.2 • tee-sys capturing: Python writes to sys.stdout and sys.stderr will be captured, however the writes will also be passed-through to the actual sys.stdout and sys.stderr. This allows output to be ‘live printed’ and capturedforpluginuse,suchasjunitxml(newinpytest5.4). Youcaninfluenceoutputcapturingmechanismsfromthecommandline: pytest -s # disable all capturing pytest --capture=sys # replace sys.stdout/stderr with in-mem files pytest --capture=fd # also point filedescriptors 1 and 2 to temp file pytest --capture=tee-sys # combines 'sys' and '-s', capturing sys.stdout/stderr # and passing it along to the actual sys.stdout/stderr 2.11.3 Using print statements for debugging Oneprimarybenefitofthedefaultcapturingofstdout/stderroutputisthatyoucanuseprintstatementsfordebugging: # content of test_module.py def setup_function(function): print("setting up", function...
```

#### Rank 2: page 77, score 70.063, chunk `pytest-documentation-p0077-c01`

```text
pytest Documentation, Release 9.2 Otherpluginsmayaccessthe config.cacheobjecttoset/get json encodablevaluesbetweenpytestinvocations. INFO-CIRCLE Note Thispluginisenabledbydefault,butcanbedisabledifneeded: see Deactivating / unregistering a plugin by name(the internalnameforthispluginiscacheprovider). 2.9.2 Rerunning only failures or failures ﬁrst First,let’screate50testinvocationsofwhichonly2fail: # content of test_50.py import pytest @pytest.mark.parametrize("i", range(50)) def test_num(i): if i in (17, 25): pytest.fail("bad luck") Ifyourunthisforthefirsttimeyouwillseetwofailures: $ pytest -q .................F.......F........................ [100%] ================================= FAILURES ================================= _______________________________ test_num[17] _______________________________ i = 17 @pytest.mark.parametrize("i", range(50)) def test_num(i): if i in (17, 25): > py...
```

#### Rank 3: page 324, score 59.629, chunk `pytest-documentation-p0324-c01`

```text
pytest Documentation, Release 9.2 filtering(filter_) Context manager that temporarily adds the given filter to the caplog’s handler() for the ‘with’ statement block,andremovesthatfilterattheendoftheblock. Parameters filter–Acustomlogging.Filterobject. Addedinversion7.5. capsys Tutorial: How to capture stdout/stderr output capsys() Enabletextcapturingofwritestosys.stdoutandsys.stderr. The captured output is made available via capsys.readouterr() method calls, which return a (out, err) namedtuple. outanderrwillbetextobjects. Returnsaninstanceof CaptureFixture[str]. Example: def test_output(capsys): print("hello") captured = capsys.readouterr() assert captured.out == "hello\n" class CaptureFixture Objectreturnedbythe capsys, capsysbinary, capfd and capfdbinary fixtures. readouterr() Readandreturnthecapturedoutputsofar,resettingtheinternalbuffer. Returns Thecapturedcontentasanamedtuplewithou...
```

### Labeled relevant page text

- Page 149: 2 chunk(s)
  - Chunk `pytest-documentation-p0149-c01`
```text
pytest Documentation, Release 9.2
```
  - Chunk `pytest-documentation-p0149-c02`
```text
pytest Documentation, Release 9.2 pytest-allclose last release: Jul30,2019, status: 5-Production/Stable, requires: pytest PytestfixtureextendingNumpy’sallclosefunction pytest-allure-adaptor last release: Jan10,2018, status: N/A, requires: pytest(>=2.7.3) Pluginforpy.testtogenerateallurexmlreports pytest-allure-adaptor2 last release: Oct14,2020, status: N/A, requires: pytest(>=2.7.3) Pluginforpy.testtogenerateallurexmlreports pytest-allure-collection last release: Apr13,2023, status: N/A, requires: pytest pytestplugintocollectalluremarkerswithoutrunninganytests pytest-allure-dsl last release: Oct25,2020, status: 4-Beta, requires: pytest pytestplugintotestcasedocstringdlsinstructions pytest-allure-host last release: Nov03,2025, status: 3-Alpha, requires: N/A PublishAllurestaticreportstoprivateS3behindCloudFrontwithhistorypreservation pytest-allure-id2history last release: May14,2024, statu...
```

- Page 150: 2 chunk(s)
  - Chunk `pytest-documentation-p0150-c01`
```text
pytest Documentation, Release 9.2
```
  - Chunk `pytest-documentation-p0150-c02`
```text
pytest Documentation, Release 9.2 pytest-analyzer last release: Feb21,2024, status: N/A, requires: pytest<8.0.0,>=7.3.1 thispluginallowstoanalyzetestsinpytestproject,collecttestmetadataandsyncitwithtestomat.ioTCMsystem pytest-android last release: Feb21,2019, status: 3-Alpha, requires: pytest Thisfixtureprovidesaconfigured“driver”forAndroidAutomatedTesting,usinguiautomator2. pytest-anki last release: Jul31,2022, status: 4-Beta, requires: pytest(>=3.5.0) ApytestpluginfortestingAnkiadd-ons pytest-anki2 last release: Jun10,2026, status: 5-Production/Stable, requires: pytest>=7.0 ApytestpluginfortestingAnkiadd-ons pytest-annotate last release: Jun07,2022, status: 3-Alpha, requires: pytest(<8.0.0,>=3.2.0) pytest-annotate: GeneratePyAnnotateannotationsfromyourpytesttests. pytest-annotated last release: Sep30,2024, status: N/A, requires: pytest>=8.3.3 PytestplugintoallowuseofAnnotatedinteststor...
```

## 8. dev-008: How do I assert that code emits a warning?

- Relevant pages: `[154, 155]`
- Retrieved pages: `[472, 77, 93]`
- Hit: `False`

### Retrieved chunks

#### Rank 1: page 472, score 58.317, chunk `pytest-documentation-p0472-c01`

```text
pytest Documentation, Release 9.2 (continuedfrompreviouspage) b = 2 > assert A.a == b, "A.a appears not to be b" E AssertionError: A.a appears not to be b E assert 1 == 2 E + where 1 = <class 'failure_demo.TestCustomAssertMsg.test_single_line. ˓→<locals>.A'>.a failure_demo.py:263: AssertionError ____________________ TestCustomAssertMsg.test_multiline ____________________ self = <failure_demo.TestCustomAssertMsg object at 0xdeadbeef002f> def test_multiline(self): class A: a = 1 b = 2 > assert A.a == b, ( "A.a appears not to be b\nor does not appear to be b\none of those" ) E AssertionError: A.a appears not to be b E or does not appear to be b E one of those E assert 1 == 2 E + where 1 = <class 'failure_demo.TestCustomAssertMsg.test_multiline.<locals> ˓→.A'>.a failure_demo.py:270: AssertionError ___________________ TestCustomAssertMsg.test_custom_repr ___________________ self = <failure_de...
```

#### Rank 2: page 77, score 51.648, chunk `pytest-documentation-p0077-c01`

```text
pytest Documentation, Release 9.2 Otherpluginsmayaccessthe config.cacheobjecttoset/get json encodablevaluesbetweenpytestinvocations. INFO-CIRCLE Note Thispluginisenabledbydefault,butcanbedisabledifneeded: see Deactivating / unregistering a plugin by name(the internalnameforthispluginiscacheprovider). 2.9.2 Rerunning only failures or failures ﬁrst First,let’screate50testinvocationsofwhichonly2fail: # content of test_50.py import pytest @pytest.mark.parametrize("i", range(50)) def test_num(i): if i in (17, 25): pytest.fail("bad luck") Ifyourunthisforthefirsttimeyouwillseetwofailures: $ pytest -q .................F.......F........................ [100%] ================================= FAILURES ================================= _______________________________ test_num[17] _______________________________ i = 17 @pytest.mark.parametrize("i", range(50)) def test_num(i): if i in (17, 25): > py...
```

#### Rank 3: page 93, score 43.098, chunk `pytest-documentation-p0093-c01`

```text
pytest Documentation, Release 9.2 ThiswillignoreallwarningsoftypeDeprecationWarningwherethestartofthemessagematchestheregularexpres- sion".*U.*mode is deprecated". See @pytest.mark.filterwarningsand Controlling warningsformoreexamples. INFO-CIRCLE Note If warnings are configured at the interpreter level, using the PYTHONWARNINGS environment variable or the -W command-lineoption,pytestwillnotconfigureanyfiltersbydefault. Alsopytestdoesn’tfollow PEP 565suggestionofresettingallwarningfiltersbecauseitmightbreaktestsuitesthat configurewarningfiltersthemselvesbycallingwarnings.simplefilter()(see#2430foranexampleofthat). 2.12.7 Ensuring code triggers a deprecation warning You can also use pytest.deprecated_call() for checking that a certain function call triggers a Deprecation- Warning,PendingDeprecationWarningorFutureWarning: import pytest def test_myfunction_deprecated(): with pytest.deprecat...
```

### Labeled relevant page text

- Page 154: 2 chunk(s)
  - Chunk `pytest-documentation-p0154-c01`
```text
pytest Documentation, Release 9.2
```
  - Chunk `pytest-documentation-p0154-c02`
```text
pytest Documentation, Release 9.2 pytest-ast-back-to-python last release: Sep29,2019, status: 4-Beta, requires: N/A ApluginforpytestdevstoviewhowassertionrewritingrecodestheAST pytest-asteroid last release: Aug15,2022, status: N/A, requires: pytest(>=6.2.5,<8.0.0) PyTestpluginfordocker-basedtestingondatabaseimages pytest-astropy last release: Aug03,2026, status: 5-Production/Stable, requires: pytest>=4.6 Meta-packagecontainingdependenciesfortesting pytest-astropy-header last release: Sep06,2022, status: 3-Alpha, requires: pytest(>=4.6) pytestplugintoadddiagnosticinformationtotheheaderofthetestoutput pytest-ast-transformer last release: May04,2019, status: 3-Alpha, requires: pytest pytest_async last release: Feb26,2020, status: N/A, requires: N/A pytest-async-Runyourcoroutineineventloopwithoutdecorator pytest-async-benchmark last release: May28,2025, status: N/A, requires: pytest>=8.3.5 p...
```

- Page 155: 2 chunk(s)
  - Chunk `pytest-documentation-p0155-c01`
```text
pytest Documentation, Release 9.2
```
  - Chunk `pytest-documentation-p0155-c02`
```text
pytest Documentation, Release 9.2 pytest-atf-allure last release: Nov29,2023, status: N/A, requires: pytest(>=7.4.2,<8.0.0) 基于allure-pytest进行自定义 pytest-atomic last release: Nov24,2018, status: 4-Beta, requires: N/A Skiprestoftestsifprevioustestfailed. pytest-atstack last release: Jan02,2025, status: 4-Beta, requires: pytest>=6.2.0 Asimpleplugintousewithpytest pytest-attempt-summary last release: Jan04,2026, status: N/A, requires: pytest>=7.0 EnhancedAllureAttemptSummaryforPlaywright+Pytest pytest-attrib last release: May24,2016, status: 4-Beta, requires: N/A pytestplugintoselecttestsbasedonattributessimilartothenose-attribplugin pytest-attributes last release: Jun24,2024, status: 4-Beta, requires: pytest>=6.2.0 Apluginthatallowsuserstoaddattributestotheirtests. Theseattributescanthenbereferencedbyfixturesorthe testitself. pytest-audioeval last release: Mar18,2026, status: 4-Beta, require...
```

## 9. dev-009: How do I select tests by keyword expression?

- Relevant pages: `[25, 26]`
- Retrieved pages: `[77, 79, 13]`
- Hit: `False`

### Retrieved chunks

#### Rank 1: page 77, score 55.820, chunk `pytest-documentation-p0077-c01`

```text
pytest Documentation, Release 9.2 Otherpluginsmayaccessthe config.cacheobjecttoset/get json encodablevaluesbetweenpytestinvocations. INFO-CIRCLE Note Thispluginisenabledbydefault,butcanbedisabledifneeded: see Deactivating / unregistering a plugin by name(the internalnameforthispluginiscacheprovider). 2.9.2 Rerunning only failures or failures ﬁrst First,let’screate50testinvocationsofwhichonly2fail: # content of test_50.py import pytest @pytest.mark.parametrize("i", range(50)) def test_num(i): if i in (17, 25): pytest.fail("bad luck") Ifyourunthisforthefirsttimeyouwillseetwofailures: $ pytest -q .................F.......F........................ [100%] ================================= FAILURES ================================= _______________________________ test_num[17] _______________________________ i = 17 @pytest.mark.parametrize("i", range(50)) def test_num(i): if i in (17, 25): > py...
```

#### Rank 2: page 79, score 39.691, chunk `pytest-documentation-p0079-c01`

```text
pytest Documentation, Release 9.2 (continuedfrompreviouspage) i = 17 @pytest.mark.parametrize("i", range(50)) def test_num(i): if i in (17, 25): > pytest.fail("bad luck") E Failed: bad luck test_50.py:7: Failed _______________________________ test_num[25] _______________________________ i = 25 @pytest.mark.parametrize("i", range(50)) def test_num(i): if i in (17, 25): > pytest.fail("bad luck") E Failed: bad luck test_50.py:7: Failed ========================= short test summary info ========================== FAILED test_50.py::test_num[17] - Failed: bad luck FAILED test_50.py::test_num[25] - Failed: bad luck ======================= 2 failed, 48 passed in 0.12s ======================= New --nf, --new-firstoption: runnewtestsfirstfollowedbytherestofthetests,inbothcasestestsarealsosorted bythefilemodifiedtime,withmorerecentfilescomingfirst. 2.9.3 Behavior when no tests failed in the last ru...
```

#### Rank 3: page 13, score 38.545, chunk `pytest-documentation-p0013-c01`

```text
CHAPTER TWO HOW-TO GUIDES 2.1 How to invoke pytest SHARE See also Complete pytest command-line flags reference Ingeneral,pytestisinvokedwiththecommandpytest(seebelowfor other ways to invoke pytest). Thiswillexecuteall testsinallfileswhosenamesfollowtheformtest_*.pyor*_test.pyinthecurrentdirectoryanditssubdirectories. Moregenerally,pytestfollows standard test discovery rules. 2.1.1 Specifying which tests to run Pytestsupportsseveralwaystorunandselecttestsfromthecommand-lineorfromafile(seebelowfor reading arguments from file). Run tests in a module pytest test_mod.py Run tests in a directory pytest testing/ Run tests by keyword expressions pytest -k 'MyClass and not method' Thiswillruntestswhichcontainnamesthatmatchthegiven string expression(case-insensitive),whichcanincludePython operatorsthatusefilenames,classnamesandfunctionnamesasvariables. TheexampleabovewillrunTestMyClass. test_somet...
```

### Labeled relevant page text

- Page 25: 2 chunk(s)
  - Chunk `pytest-documentation-p0025-c01`
```text
pytest Documentation, Release 9.2 (continuedfrompreviouspage) [ [1, 2, 5], [2, 3, 8], [5, 3, 18], ], ) def test_foo(a, b, result): assert foo(a, b) == result 2.2.8 Assertion introspection details Reportingdetailsaboutafailingassertionisachievedbyrewritingassertstatementsbeforetheyarerun. Rewrittenassert statementsputintrospectioninformationintotheassertionfailuremessage. pytestonlyrewritestestmodulesdirectly discovered by its test collection process, so asserts in supporting modules which are not themselves test modules will not be rewritten. Youcanmanuallyenableassertionrewritingforanimportedmodulebycalling register_assert_rewritebeforeyouimport it(agoodplacetodothatisinyourrootconftest.py). Forfurtherinformation,BenjaminPetersonwroteupBehindthescenesofpytest’snewassertionrewriting. Assertion rewriting caches ﬁles on disk pytestwillwritebacktherewrittenmodulestodiskforcaching. Youcandis...
```
  - Chunk `pytest-documentation-p0025-c02`
```text
of assertion introspection, the only change is that the .pyc files won’t be cached on disk. Additionally, rewriting will silently skip caching if it cannot write new .pyc files, e.g. in a read-only filesystem or a zipfile. Disabling assert rewriting pytest rewrites test modules on import by using an import hook to write new pyc files. Most of the time this works transparently. However,ifyouareworkingwiththeimportmachineryyourself,theimporthookmayinterfere. Ifthisisthecaseyouhavetwooptions: • DisablerewritingforaspecificmodulebyaddingthestringPYTEST_DONT_REWRITEtoitsdocstring. • Disablerewritingforallmodulesbyusing --assert=plain. 2.3 How to use ﬁxtures SHARE See also About fixtures 2.3. How to use ﬁxtures 21
```

- Page 26: 1 chunk(s)
  - Chunk `pytest-documentation-p0026-c01`
```text
pytest Documentation, Release 9.2 SHARE See also Fixtures reference 2.3.1 “Requesting” ﬁxtures Atabasiclevel,testfunctionsrequestfixturestheyrequirebydeclaringthemasarguments. Whenpytestgoestorunatest, itlooksattheparametersinthattestfunction’ssignature, andthensearchesforfixtures thathavethesamenamesasthoseparameters. Oncepytestfindsthem,itrunsthosefixtures,captureswhattheyreturned (ifanything),andpassesthoseobjectsintothetestfunctionasarguments. Quick example import pytest class Fruit: def __init__(self, name): self.name = name self.cubed = False def cube(self): self.cubed = True class FruitSalad: def __init__(self, *fruit_bowl): self.fruit = fruit_bowl self._cube_fruit() def _cube_fruit(self): for fruit in self.fruit: fruit.cube() # Arrange @pytest.fixture def fruit_bowl(): return [Fruit("apple"), Fruit("banana")] def test_fruit_salad(fruit_bowl): # Act fruit_salad = FruitSalad(*fruit...
```

## 10. dev-010: How do I use conftest.py to share fixtures?

- Relevant pages: `[113, 114]`
- Retrieved pages: `[77, 106, 473]`
- Hit: `False`

### Retrieved chunks

#### Rank 1: page 77, score 62.837, chunk `pytest-documentation-p0077-c01`

```text
pytest Documentation, Release 9.2 Otherpluginsmayaccessthe config.cacheobjecttoset/get json encodablevaluesbetweenpytestinvocations. INFO-CIRCLE Note Thispluginisenabledbydefault,butcanbedisabledifneeded: see Deactivating / unregistering a plugin by name(the internalnameforthispluginiscacheprovider). 2.9.2 Rerunning only failures or failures ﬁrst First,let’screate50testinvocationsofwhichonly2fail: # content of test_50.py import pytest @pytest.mark.parametrize("i", range(50)) def test_num(i): if i in (17, 25): pytest.fail("bad luck") Ifyourunthisforthefirsttimeyouwillseetwofailures: $ pytest -q .................F.......F........................ [100%] ================================= FAILURES ================================= _______________________________ test_num[17] _______________________________ i = 17 @pytest.mark.parametrize("i", range(50)) def test_num(i): if i in (17, 25): > py...
```

#### Rank 2: page 106, score 56.159, chunk `pytest-documentation-p0106-c01`

```text
pytest Documentation, Release 9.2 4. by loading all plugins registered through installed third-party package entry points, unless the PYTEST_DIS- ABLE_PLUGIN_AUTOLOADenvironmentvariableisset. 5. byloadingallpluginsspecifiedthroughthe PYTEST_PLUGINSenvironmentvariable. 6. byloadingall“initial”conftest.pyfiles: • determine the test paths: specified on the command line, otherwise in testpaths if defined and running fromtherootdir,otherwisethecurrentdir • for each test path, load conftest.py and test*/conftest.py relative to the directory part of the test path, if they exist. Before a conftest.py file is loaded, load conftest.py files in its parent directories uptothe --confcutdir limit. When--confcutdirisnotprovided,thecutoffdefaultstothedirectory containing the config file, or to the rootdir if no config file is found. After a conftest.py file is loaded, recursivelyloadallpluginsspecifiedi...
```

#### Rank 3: page 473, score 52.614, chunk `pytest-documentation-p0473-c02`

```text
pytest Documentation, Release 9.2 (continuedfrompreviouspage) FAILED failure_demo.py::TestFailing::test_simple - assert 42 == 43 FAILED failure_demo.py::TestFailing::test_simple_multiline - assert 42 == 54 FAILED failure_demo.py::TestFailing::test_not - assert not 42 FAILED failure_demo.py::TestSpecialisedExplanations::test_eq_text - Asser... FAILED failure_demo.py::TestSpecialisedExplanations::test_eq_similar_text FAILED failure_demo.py::TestSpecialisedExplanations::test_eq_multiline_text FAILED failure_demo.py::TestSpecialisedExplanations::test_eq_long_text - ... FAILED failure_demo.py::TestSpecialisedExplanations::test_eq_long_text_multiline FAILED failure_demo.py::TestSpecialisedExplanations::test_eq_list - asser... FAILED failure_demo.py::TestSpecialisedExplanations::test_eq_list_long - ... FAILED failure_demo.py::TestSpecialisedExplanations::test_eq_dict - Asser... FAILED failure_d...
```

### Labeled relevant page text

- Page 113: 2 chunk(s)
  - Chunk `pytest-documentation-p0113-c01`
```text
pytest Documentation, Release 9.2 2.16.3 hook wrappers: executing around other hooks pytestpluginscanimplementhookwrapperswhichwraptheexecutionofotherhookimplementations. Ahookwrapper isageneratorfunctionwhichyieldsexactlyonce. Whenpytestinvokeshooksitfirstexecuteshookwrappersandpasses thesameargumentsastotheregularhooks. At the yield point of the hook wrapper pytest will execute the next hook implementations and return their result to the yieldpoint,orwillpropagateanexceptioniftheyraised. Hereisanexampledefinitionofahookwrapper: import pytest @pytest.hookimpl(wrapper=True) def pytest_pyfunc_call(pyfuncitem): do_something_before_next_hook_executes() # If the outcome is an exception, will raise the exception. res = yield new_res = post_process_result(res) # Override the return value to the plugin system. return new_res Thehookwrapperneedstoreturnaresultforthehook,orraiseanexception. Inman...
```
  - Chunk `pytest-documentation-p0113-c02`
```text
Ifthehookimplementationfailedwithanexception,thewrappercanhandlethatexceptionusingatry-catch-finally aroundtheyield,bypropagatingit,suppressingit,orraisingadifferentexceptionentirely. Formoreinformation,consultthepluggydocumentationabouthookwrappers. 2.16.4 Hook function ordering / call example Foranygivenhookspecificationtheremaybemorethanoneimplementationandwethusgenerallyviewhookexecution asa1:NfunctioncallwhereNisthenumberofregisteredfunctions. Therearewaystoinfluenceifahookimplementation comesbeforeorafterothers,i.e. thepositionintheN-sizedlistoffunctions: # Plugin 1 @pytest.hookimpl(tryfirst=True) def pytest_collection_modifyitems(items): # will execute as early as possible ... # Plugin 2 @pytest.hookimpl(trylast=True) def pytest_collection_modifyitems(items): # will execute as late as possible ... (continuesonnextpage) 2.16. Writing hook functions 109
```

- Page 114: 2 chunk(s)
  - Chunk `pytest-documentation-p0114-c01`
```text
pytest Documentation, Release 9.2 (continuedfrompreviouspage) # Plugin 3 @pytest.hookimpl(wrapper=True) def pytest_collection_modifyitems(items): # will execute even before the tryfirst one above! try: return (yield) finally: # will execute after all non-wrappers executed ... Hereistheorderofexecution: 1. Plugin3’spytest_collection_modifyitemscalleduntiltheyieldpointbecauseitisahookwrapper. 2. Plugin1’spytest_collection_modifyitemsiscalledbecauseitismarkedwithtryfirst=True. 3. Plugin2’spytest_collection_modifyitemsiscalledbecauseitismarkedwithtrylast=True(butevenwithoutthis markitwouldcomeafterPlugin1). 4. Plugin3’spytest_collection_modifyitemsthenexecutingthecodeaftertheyieldpoint. Theyieldreceivestheresult fromcallingthenon-wrappers,orraisesanexceptionifthenon-wrappersraised. It’spossibletousetryfirstandtrylastalsoonhookwrappersinwhichcaseitwillinfluencetheorderingofhook wrappersamonge...
```
  - Chunk `pytest-documentation-p0114-c02`
```text
ickoverviewonhowtoaddnewhooksandhowtheyworkingeneral,butamorecompleteoverviewcan befoundinthepluggydocumentation. Pluginsandconftest.pyfilesmaydeclarenewhooksthatcanthenbeimplementedbyotherpluginsinordertoalter behaviourorinteractwiththenewplugin: pytest_addhooks(pluginmanager) Called at plugin registration time to allow adding new hooks via a call to pluginmanager. add_hookspecs(module_or_class, prefix). Parameters pluginmanager–Thepytestpluginmanager. 110 Chapter 2. How-to guides
```
