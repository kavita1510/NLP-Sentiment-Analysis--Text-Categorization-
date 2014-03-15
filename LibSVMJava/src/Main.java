import java.io.IOException;


public class Main {

		public static void main(String args[]) throws IOException{

			/*svm_train svm_train = new svm_train();
            svm_train.run(new String[] { "-t", "0", "outputs/train_" + i,
                            "outputs/train_" + i + ".model" });
            svm_predict.main(new String[] { "outputs/test_" + i + ".t",
                            "outputs/train_" + i + ".model", "outputs/testout_" + i });
            */
            svm_train svm_train = new svm_train();
            svm_train.run(new String[] { "-t", "0", "SVMTraindataC.txt" ,"ModelC1.txt" });
            svm_predict.main(new String[] { "SVMTestdataC.txt",
                             "ModelC1.txt", "ResultC1.txt"});

            svm_train svm_train2 = new svm_train();
            svm_train.run(new String[] { "-t", "0", "SVMTraindataC01.txt" ,"ModelC2.txt" });
            svm_predict.main(new String[] { "SVMTestdataC01.txt",
                             "ModelC2.txt", "ResultC2.txt"});

            svm_train svm_train3 = new svm_train();
            svm_train.run(new String[] { "-t", "0", "SVMTraindataC02.txt" ,"ModelC3.txt" });
            svm_predict.main(new String[] { "SVMTestdataC02.txt",
                             "ModelC3.txt", "ResultC3.txt"});

            svm_train svm_train4 = new svm_train();
            svm_train.run(new String[] { "-t", "0", "SVMTraindataC03.txt" ,"ModelC4.txt" });
            svm_predict.main(new String[] { "SVMTestdataC03.txt",
                             "ModelC4.txt", "ResultC4.txt"});

            svm_train svm_train5 = new svm_train();
            svm_train.run(new String[] { "-t", "0", "SVMTraindata04.txt" ,"Model5.txt" });
            svm_predict.main(new String[] { "SVMTestdata04.txt",
                             "Model5.txt", "Result5.txt"});
		}
}
