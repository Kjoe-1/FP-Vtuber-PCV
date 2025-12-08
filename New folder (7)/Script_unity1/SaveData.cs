// Reference: https://youtu.be/uD7y4T4PVk0
using System.Collections.Generic;
using UnityEngine;

public static class SaveDataManager
{
    public static bool SaveJsonData(IEnumerable<ISaveable> a_Saveables)
    {
        MaoPref MaoPref = new MaoPref();
        foreach (var saveable in a_Saveables)
        {
            saveable.PopulateSaveData(MaoPref);
        }

        bool isSuccess = FileManager.WriteToFile("MaoPrefData01.dat", MaoPref.ToJson());

        if (isSuccess)
        {
            Debug.Log("Save successful");
        }

        return isSuccess;
    }

    public static bool LoadJsonData(IEnumerable<ISaveable> a_Saveables)
    {

        bool isSuccess = FileManager.LoadFromFile("MaoPrefData01.dat", out var json);

        if (isSuccess)
        {
            MaoPref MaoPref = new MaoPref();
            MaoPref.LoadFromJson(json);

            foreach (var saveable in a_Saveables)
            {
                saveable.LoadFromSaveData(MaoPref);
            }

            Debug.Log("Load complete");
        }

        return isSuccess;
    }
}